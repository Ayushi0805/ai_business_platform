"""
Phase 7 – CrewAI Invoice Analysis Agent.

Uses the HuggingFace NLP service to extract and validate invoice fields.
"""
import os
from crewai import Agent, LLM
from crewai.tools import tool
from app.services.invoice_nlp import parse_invoice_text
from app.llm.base_llm import get_llm

@tool("Invoice_Parser")
def invoice_nlp_tool(invoice_text: str) -> str:
    data = parse_invoice_text(invoice_text)
    return str(data)

invoice_agent = Agent(
    role='Invoice Analyst',
    goal='Extract and validate key fields from invoice documents using NLP',
    backstory='You are a senior accounts payable specialist who verifies invoices for accuracy, consistency, and fraud indicators.',
    tools=[invoice_nlp_tool],
    llm=LLM(
        model=f"openai/{os.environ.get('VLLM_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2')}",
        base_url=os.environ.get('VLLM_API_BASE')
    ),
    verbose=True
)
