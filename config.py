from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = "ollama/deepseek-r1:latest",
    base_url = "http://localhost:11435",
    temperature = 0.2
    )