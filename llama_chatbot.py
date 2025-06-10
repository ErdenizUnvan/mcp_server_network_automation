from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

# Ollama modeli ayarı
LLAMA_MODEL_URL = "http://127.0.0.1:11434"
MODEL_NAME = "llama3.2"
Settings.llm = Ollama(model=MODEL_NAME, base_url=LLAMA_MODEL_URL, request_timeout=120.0)

# Test sorgusu
query = input('query: ')
#"What is the capital of France?"
# Ollama nesnesi
llama_model = Settings.llm

# Metotları sırayla deneyelim
try:
    print("Testing `complete` method:")
    response = llama_model.complete(prompt=query)
    print(f"Response: {response}")
except Exception as e:
    print("`complete` method failed:", e)
