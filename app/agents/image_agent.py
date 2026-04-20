import os
from crewai import Agent, LLM
from crewai.tools import tool
from app.services.image_cv import analyze_image
from app.llm.base_llm import get_llm

@tool("Image_Analyzer")
def image_analysis_tool(image_path: str) -> str:
    result = analyze_image(image_path)
    return str(result)

image_agent = Agent(
    role='Computer Vision Analyst',
    goal='Verify that uploaded product images are authentic and match the order',
    backstory='You are a visual inspection expert who uses AI to detect objects in images and flag mismatches or suspicious content.',
    tools=[image_analysis_tool],
    llm=LLM(
        model=f"openai/{os.environ.get('VLLM_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2')}",
        base_url=os.environ.get('VLLM_API_BASE')
    ),
    verbose=True
)
