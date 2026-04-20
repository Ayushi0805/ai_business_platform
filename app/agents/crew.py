"""
Phase 7 — CrewAI Crew orchestrator.

Composes all three agents (Fraud, Invoice, Image) into a single Crew
that runs as a sequential pipeline and returns a combined analysis report.
"""
from crewai import Crew, Task
from app.agents.fraud_agent import fraud_agent
from app.agents.invoice_agent import invoice_agent
from app.agents.image_agent import image_agent

def run_crew(order_data: dict) -> dict:
    fraud_task = Task(
        description=f"Analyze this order for fraud: {order_data}",
        agent=fraud_agent,
        expected_output='A verdict: FRAUD DETECTED or Order appears legitimate'
    )

    invoice_task = Task(
        description=f"Parse and validate this invoice text: {order_data.get('invoice_text', '')}",
        agent=invoice_agent,
        expected_output='Extracted invoice fields as a dictionary'
    )

    image_task = Task(
        description=f"Analyze the product image at: {order_data.get('image_path', 'N/A')}",
        agent=image_agent,
        expected_output='Detected objects and confidence score'
    )

    crew = Crew(
        agents=[fraud_agent, invoice_agent, image_agent],
        tasks=[fraud_task, invoice_task, image_task],
        verbose=True
    )

    result = crew.kickoff()

    return {
        'crew_report': str(result),
        'fraud_report': 'See crew report',
        'invoice_report': 'See crew report',
        'image_report': 'See crew report'
    }
