"""
Phase 7 – CrewAI Fraud Detection Agent.

Install: pip install crewai

This agent wraps the sklearn/rule-based fraud service as a CrewAI Tool,
so it can be called autonomously within the crew.
"""
import os
from crewai import Agent, LLM
from crewai.tools import tool
from app.services.fraud import detect_fraud
from app.llm.base_llm import get_llm

@tool("Fraud_Detector")
def fraud_detection_tool(total_price: float, quantity: int, user_id: int) -> str:
    result = detect_fraud(total_price, quantity, user_id)
    if result:
        return 'FRAUD DETECTED'
    return 'Order appears legitimate'

fraud_agent = Agent(
    role='Fraud Detection Specialist',
    goal='Analyze order financial data and detect potentially fraudulent transactions',
    backstory='You are an expert forensic accountant and fraud analyst with 15 years of experience. You use machine learning and pattern recognition to identify suspicious orders.',
    tools=[fraud_detection_tool],
    llm=LLM(
        model=f"openai/{os.environ.get('VLLM_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2')}",
        base_url=os.environ.get('VLLM_API_BASE')
    ),
    verbose=True
)
