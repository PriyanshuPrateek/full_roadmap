from pydantic import BaseModel, Field
from typing import List


class Node(BaseModel):
    id: str = Field(description="Unique identifier of topic")
    title: str = Field(description="Topic name")
    description: str = Field(description="Topic explanation")
    estimated_hours: int = Field(description="Estimated learning hours")
    level: str = Field(description="Beginner, Intermediate, or Advanced")


class Edge(BaseModel):
    source: str = Field(description="Source node id")
    target: str = Field(description="Target node id")


class Roadmap(BaseModel):
    nodes: List[Node]
    edges: List[Edge]