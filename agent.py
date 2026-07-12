import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.planner import run_planner
from agents.researcher import run_researcher
from agents.synthesizer import run_synthesizer
from eval import evaluate_report
from memory import save_to_memory, get_relevant_memory
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0.3
    )

def save_report(report, scores: dict) -> str:
    from datetime import datetime
    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output = {
        "topic": report.topic,
        "summary": report.summary,
        "key_insights": report.key_insights,
        "gaps": report.gaps,
        "quality_score": report.quality_score,
        "eval_scores": scores,
        "findings": [
            {
                "question": f.question,
                "answer": f.answer,
                "sources": f.sources,
                "confidence": f.confidence
            }
            for f in report.findings
        ],
        "timestamp": report.timestamp
    }
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    return filename

def run(topic: str):
    print(f"\n🚀 Starting research: {topic}")
    print("=" * 60)

    llm = get_llm()

    # Check memory for prior context
    prior_context = get_relevant_memory(topic)
    if prior_context:
        print(f"\n💾 Found relevant prior research")
        topic_with_context = f"{topic}\n\nContext from prior research:\n{prior_context}"
    else:
        topic_with_context = topic

    # Step 1 — Planner breaks topic into subtasks
    tasks = run_planner(topic_with_context, llm)

    # Step 2 — Researchers run in sequence
    with ThreadPoolExecutor(max_workers=3) as executor:
        findings = list(executor.map(
        lambda task: run_researcher(task, llm),
        tasks
    ))

    # Step 3 — Synthesizer combines findings
    report = run_synthesizer(topic, findings, llm)

    # Step 4 — Evaluator scores the report
    scores = evaluate_report(report, llm)

    # Step 5 — Save report and update memory
    filename = save_report(report, scores)
    save_to_memory(report)

    print(f"\n{'=' * 60}")
    print(f"📄 FINAL REPORT: {topic}")
    print(f"{'=' * 60}")
    print(f"\nSummary:\n{report.summary}")
    print(f"\nKey Insights:")
    for insight in report.key_insights:
        print(f"  • {insight}")
    print(f"\nGaps:")
    for gap in report.gaps:
        print(f"  • {gap}")
    print(f"\nQuality: {report.quality_score} | Eval Overall: {scores['overall']}")
    print(f"Saved to: {filename}")
    
    return {
        "topic": report.topic,
        "summary": report.summary,
        "key_insights": report.key_insights,
        "gaps": report.gaps,
        "quality_score": report.quality_score,
        "eval_scores": scores,
        "filename": filename
    }

if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run(topic)