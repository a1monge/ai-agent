from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class ResearchTask(BaseModel):
    """A single research subtask assigned to a researcher agent."""
    id: int
    question: str
    focus_area: str

class ResearchFinding(BaseModel):
    """Findings from a single researcher agent."""
    task_id: int
    question: str
    answer: str
    sources: List[str]
    confidence: float = Field(ge=0.0, le=1.0)

class ResearchReport(BaseModel):
    """Final structured report produced by the synthesizer."""
    topic: str
    summary: str
    findings: List[ResearchFinding]
    key_insights: List[str]
    gaps: List[str]
    quality_score: float = Field(ge=0.0, le=1.0)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())