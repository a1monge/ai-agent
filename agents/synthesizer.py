from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from models import ResearchFinding, ResearchReport
import json

SYNTHESIZER_PROMPT = """You are a senior analyst writing a technical research report.

Rules:
- Write like a human analyst, not an AI
- Direct declarative sentences only
- No filler phrases: "it is worth noting", "in conclusion", "delve into", "game-changing"
- Be specific — cite facts not generalities
- State uncertainty directly when it exists

From the research findings provided, produce:
1. A 3-5 sentence executive summary in plain prose
2. 3-5 specific insights a Google search wouldn't give you
3. 2-3 genuine gaps the research didn't answer
4. An honest quality score 0.0 to 1.0

Respond with ONLY this JSON:
{
    "summary": "...",
    "key_insights": ["...", "...", "..."],
    "gaps": ["...", "..."],
    "quality_score": 0.0
}"""

def run_synthesizer(topic: str, findings: list[ResearchFinding], llm: ChatGoogleGenerativeAI) -> ResearchReport:
    findings_text = ""
    for f in findings:
        findings_text += f"\n--- Finding {f.task_id} (confidence: {f.confidence}) ---\n"
        findings_text += f"Question: {f.question}\n"
        findings_text += f"Answer: {f.answer}\n"
        findings_text += f"Sources: {', '.join(f.sources) if f.sources else 'none'}\n"

    messages = [
        SystemMessage(content=SYNTHESIZER_PROMPT),
        HumanMessage(content=f"Topic: {topic}\n\n{findings_text}")
    ]

    response = llm.invoke(messages)

    content = response.content
    if isinstance(content, list):
        first = content[0]
        content = first.get("text", "") if isinstance(first, dict) else str(first)

    content = content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]

    data = json.loads(content.strip())

    return ResearchReport(
        topic=topic,
        summary=data["summary"],
        findings=findings,
        key_insights=data["key_insights"],
        gaps=data["gaps"],
        quality_score=data["quality_score"]
    )