import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
import os
import time
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    pipeline
)
import ast
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings


MODEL_DIR = r"C:\Users\Dell\llama3_2\mcp\project\facebook-bart-large-mnli"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_DIR,
    local_files_only=True
)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_DIR,
    local_files_only=True
)

classifier = pipeline(
    "zero-shot-classification",
    model=model,
    tokenizer=tokenizer,
    hypothesis_template="This request is about {}.",
)

candidate_labels = [
    "detect device type",
    "get device backup",
    "other"
]

system_prompt = (
    "You are a function-calling AI agent.\n"
    "The function you need to call will be selected according to the user's input for you and it will be informed to you\n"
    "Only provide the outcome of the function, do not make any additonal comments or statements\n"
)

chat_model  = ChatOllama(model="llama3.2").with_config({"system_prompt": system_prompt})

LLAMA_MODEL_URL = "http://127.0.0.1:11434"
MODEL_NAME = "llama3.2"
Settings.llm = Ollama(model=MODEL_NAME, base_url=LLAMA_MODEL_URL, request_timeout=120.0)

async def main():
    while True:
        user_input = input("\nQuery (exit to quit): ")

        if not user_input or user_input.isspace():
            print('please type your query.')
        elif user_input.lower() in ['quit','exit','bye']:
            print('bye')
            break
        else:
            result = classifier(user_input, candidate_labels)
            top_label = result['labels'][0]
            top_score = result['scores'][0]
            THRESHOLD = 0.55
            #else:
            while True:
                if top_label == 'other' or top_score < THRESHOLD:
                    print('Out of scope as function!')
                    break

                elif top_label=='detect device type':
                    top_label='detect_device_type'
                    query='detect device type'
                    print(top_label)

                elif top_label=='get device backup':
                    top_label='backup_device'
                    query='get device backup'
                    print(top_label)

                input_query = (
                    f"the sentence is: \"{user_input}.\" "
                    "Extract the values of keys for ip, username and password from this sentence. "
                    "If you can not find the value for ip, username or password, then use None as value of the key instead. "
                    "Return only the result values either as matching ones or as None in a dictionary as "
                    "If the match of password contains special characters like !#@_)(*&^%$, include them as part of the password. "
                    "{'ip':'','username':'','password':''}. Do not generate code. Do not return anything else except the result dictionary!"
                )
                llama_model = Settings.llm

                # Metotları sırayla deneyelim
                try:
                    response = llama_model.complete(prompt=input_query)
                except Exception as e:
                    print(f"model llama did not work:\n{e}\n")
                    break
                try:
                    result_dict = ast.literal_eval(str(response))
                except Exception as e:
                    print(f"Error occured while transforming data:{e}\n")
                    print('error for ip, username or password ')
                    break
                        #raise ValueError("IP, username or password info invalid.")
                print(result_dict)
                #print(type(result_dict))
                ip = result_dict['ip']
                username = result_dict['username']
                password = result_dict['password']

                content=f"{query} for ip:{ip} user:{username} pass:{password}"
                print(content)
                print(f'top_label:{top_label}')

                server_params = StdioServerParameters(
                    command="python",
                    args=["sso_network_function_tools_mcp_server.py"],
                )
                async with stdio_client(server_params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        tools = await load_mcp_tools(session)
                        selected_tools = [tool for tool in tools if tool.name==top_label]

                        agent = create_react_agent(chat_model, selected_tools)

                        msg = {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": content
                                }
                            ]
                        }

                        response = await agent.ainvoke(msg)

                        print("\nResponse:")
                        tool_output_found = False
                        for m in response["messages"]:
                            if m.type == "tool":
                                print(m.content)
                                tool_output_found = True

                        if not tool_output_found:
                            print("No function output was returned.")
                        break
if __name__ == "__main__":
    asyncio.run(main())
