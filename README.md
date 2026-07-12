# Multi-Agent Research System

A research automation system built with Python and LangGraph that uses multiple specialized AI agents to research any topic, synthesize findings, and evaluate output quality.

## Architecture

User Input
↓
Planner Agent → breaks topic into 3 focused sub-questions
↓
Researcher Agents → 3 agents run in parallel, each searches the web independently
↓
Synthesizer Agent → combines findings into a structured report
↓
Evaluator Agent → scores report quality across 4 dimensions
↓
JSON Report + Memory

## Tech Stack

- Python 3.12
- LangGraph — agent orchestration
- Google Gemini — LLM
- DuckDuckGo — free web search tool
- Flask — web UI
- Pydantic — structured output validation

## Features

- Multi-agent pipeline with specialized roles (planner, researcher, synthesizer, evaluator)
- Parallel researcher execution using Python's ThreadPoolExecutor
- Persistent memory — injects prior research context into new sessions
- Structured JSON output with confidence scoring per finding
- External evaluator agent scores output across accuracy, coverage, clarity, and insight
- Retry logic for resilient agent execution
- Flask web UI with async polling

## Getting Started

```bash
git clone https://github.com/a1monge/ai-agent.git
cd ai-agent
python -m venv venv
source venv/Scripts/activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
```

**Run via terminal:**

```bash
python agent.py
```

**Run via web UI:**

```bash
python app.py
# Open http://localhost:5000
```

## Project Structure

ai-agent/
├── agent.py # Orchestrator — coordinates all agents
├── app.py # Flask web UI
├── eval.py # Evaluator agent
├── memory.py # Session memory
├── models.py # Pydantic schemas
├── prompts.py # System prompts
├── tools.py # Search and save tools
└── agents/
├── planner.py # Breaks topic into subtasks
├── researcher.py # Researches one subtask
└── synthesizer.py # Combines findings into report

## Sample Output

```json
{
  "topic": "cloud computing",
  "summary": "...",
  "key_insights": ["...", "..."],
  "gaps": ["...", "..."],
  "quality_score": 0.85,
  "eval_scores": {
    "accuracy": 0.8,
    "coverage": 0.85,
    "clarity": 0.75,
    "insight": 0.7,
    "overall": 0.77
  }
}
```
