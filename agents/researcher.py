from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from models import ResearchTask, ResearchFinding
from tools import search_web
import json

RESEARCHER_PROMPT = """You are a research specialist. You have one question to answer thoroughly.

Search at least 2-3 times with different queries, synthesize what you find, and rate your confidence.

End your response with exactly this block:
FINDINGS_JSON:
{
    "answer": "your answer here",
    "sources": ["url1", "url2"],
    "confidence": 0.85
}"""

def run_researcher(task: ResearchTask, llm: ChatGoogleGenerativeAI) -> ResearchFinding:
    agent = create_react_agent(llm, [search_web])

    result = agent.invoke({
        "messages": [
            {"role": "system", "content": RESEARCHER_PROMPT},
            {"role": "user", "content": f"Question: {task.question}\nFocus: {task.focus_area}"}
        ]
    })

    content = result["messages"][-1].content
    if isinstance(content, list):
        content = " ".join(
            b.get("text", "") if isinstance(b, dict) else str(b)
            for b in content
        )

    data = {"answer": content, "sources": [], "confidence": 0.7}
    if "FINDINGS_JSON:" in content:
        try:
            json_str = content.split("FINDINGS_JSON:")[1].strip()
            if "```" in json_str:
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]
            data = json.loads(json_str.strip())
        except Exception:
            pass

    return ResearchFinding(
        task_id=task.id,
        question=task.question,
        answer=data.get("answer", content),
        sources=data.get("sources", []),
        confidence=data.get("confidence", 0.7)
    )