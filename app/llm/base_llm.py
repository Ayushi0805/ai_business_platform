"""
Phase 6 — LLM loader (Ollama local or HuggingFace pipeline).

Recommended local model: mistral:7b via Ollama
  1. Install Ollama: https://ollama.com
  2. Run: ollama pull mistral
  3. Ollama server starts automatically at http://localhost:11434

Install: pip install langchain-community
"""
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        vllm_api_base = os.environ.get('VLLM_API_BASE')
        vllm_model = os.environ.get('VLLM_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2')

        if not vllm_api_base:
            print('WARNING: VLLM_API_BASE is not set in environment. Defaulting to OpenAI schema.')
            _llm = ChatOpenAI(
                model='gpt-4o-mini',
                api_key=os.environ.get('OPENAI_API_KEY', 'EMPTY')
            )
        else:
            print(f'Connecting to Colab Transformers server at {vllm_api_base}')
            _llm = ChatOpenAI(
                model=vllm_model,
                api_key='empty',
                base_url=vllm_api_base,
                max_retries=2
            )
    return _llm

def ask_llm(prompt: str) -> str:
    llm = get_llm()
    if llm is None:
        return 'LLM not configured — Phase 6 stub.'
    return llm.invoke(prompt)
