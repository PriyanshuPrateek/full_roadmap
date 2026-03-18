from pydantic import BaseModel
from typing import List

class TopicDetails(BaseModel):
    title: str
    description: str
    subtopics: List[str]
    estimated_hours: int