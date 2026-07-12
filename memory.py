import json
import os
from models import ResearchReport
from datetime import datetime

MEMORY_FILE = "memory.json"

def load_memory() -> list[dict]:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_to_memory(report: ResearchReport) -> None:
    memory = load_memory()
    memory.append({
        "topic": report.topic,
        "summary": report.summary,
        "key_insights": report.key_insights,
        "quality_score": report.quality_score,
        "timestamp": report.timestamp
    })
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def get_relevant_memory(topic: str) -> str:
    memory = load_memory()
    if not memory:
        return ""
    
    relevant = [m for m in memory if any(
        word.lower() in m["topic"].lower() 
        for word in topic.split()
    )]
    
    if not relevant:
        return ""
    
    context = "Previous research on related topics:\n"
    for m in relevant[-3:]:
        context += f"\n- Topic: {m['topic']} (quality: {m['quality_score']})\n"
        context += f"  Summary: {m['summary']}\n"
    
    return context