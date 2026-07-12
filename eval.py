from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from models import ResearchReport
import json

EVAL_PROMPT = """You are a quality evaluator for research reports. You did NOT write this report.

Score each dimension 0.0 to 1.0. Be harsh — 0.8 is genuinely strong work.

- accuracy: facts are specific and verifiable
- coverage: topic addressed from multiple angles
- clarity: clear writing, no filler language
- insight: goes beyond a basic Google search

Respond with ONLY this JSON:
{
    "accuracy": 0.0,
    "coverage": 0.0,
    "clarity": 0.0,
    "insight": 0.0,
    "overall": 0.0,
    "critique": "one sentence on the biggest weakness"
}"""

def evaluate_report(report: ResearchReport, llm: ChatGoogleGenerativeAI) -> dict:
    report_text = f"""
Topic: {report.topic}
Summary: {report.summary}
Key Insights: {report.key_insights}
Gaps: {report.gaps}
Findings: {len(report.findings)}
Avg confidence: {sum(f.confidence for f in report.findings) / len(report.findings):.2f}
"""
    messages = [
        SystemMessage(content=EVAL_PROMPT),
        HumanMessage(content=f"Evaluate this report:\n{report_text}")
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

    scores = json.loads(content.strip())
    print(f"\n📊 Eval — overall: {scores['overall']} | critique: {scores['critique']}")
    return scores