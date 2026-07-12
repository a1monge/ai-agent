from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from models import ResearchTask
import json
import os

PLANNER_PROMPT = """You are a research planning agent. Your job is to break down a research topic into 3 specific, focused sub-questions that together will provide comprehensive coverage of the topic.

For each sub-question you must specify:
- A clear, specific question
- The focus area (e.g. "historical background", "current applications", "future trends", "challenges", "key players")

You MUST respond with ONLY valid JSON in this exact format, no other text:
{
    "tasks": [
        {"id": 1, "question": "...", "focus_area": "..."},
        {"id": 2, "question": "...", "focus_area": "..."},
        {"id": 3, "question": "...", "focus_area": "..."}
    ]
}"""

def run_planner(topic: str, llm: ChatGoogleGenerativeAI) -> list[ResearchTask]:
    """Break a research topic into structured subtasks."""
    
    messages = [
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=f"Break down this research topic into 3 sub-questions: {topic}")
    ]
    
    response = llm.invoke(messages)
    
    # Strip markdown code blocks if present
    content = response.content
    if isinstance(content, list):
        content = content[0].get("text", "") if isinstance(content[0], dict) else str(content[0])
    
    content = str(content).strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    content = content.strip()
    
    data = json.loads(content)
    tasks = [ResearchTask(**task) for task in data["tasks"]]
    
    print(f"\n📋 Planner created {len(tasks)} research tasks:")
    for task in tasks:
        print(f"  [{task.id}] {task.question} ({task.focus_area})")
    
    return tasks