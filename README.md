# mcp_server_network_automation

mcp server for sso network automation functions (detect device type and get device backup)

intent classification model: facebook-bart-large-mnli

function calling and managing model: llama 3.2 3B

Single Sign On with Ldap server 

Gradio Integration

MCP Server functions:

-detect device type 

-get serial number

-get backup

python version: 3.12.9

pip install huggingface_hub

pip install transformers

download facebook/bart-large-mnli model from hugginf face to your local env.:

python compare_intent_model_save.py

make sure ollama is working on your local env.:

for details check: setting up ollama for local llama.ipynb

pip install llama_index

pip install llama-index-llms-ollama

pip install langchain_core

pip install --upgrade --force-reinstall langgraph

pip install langchain_mcp_adapters 

pip install langchain_ollama 

pip install mcp==1.6.0

pip install fastmcp

at one terminal run:

fastmcp dev sso_network_function_tools_mcp_server.py

at another teminal run:

python network_ai_agent.py

How to use:
https://www.youtube.com/watch?v=iJVCk-fLPUI
