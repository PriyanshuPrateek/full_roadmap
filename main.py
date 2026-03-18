from fastapi import FastAPI
from roadmap_generator import generate_roadmap
from topic_generator import generate_topic

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

@app.get("/")
def home():
    return {"message": "AI Roadmap Generator Running"}

@app.get("/generate_roadmap")
def home(skill:str):
    result = generate_roadmap(skill)
    return result

@app.get("/generate_topic")
def topic_detail(topic:str):
    result = generate_topic(topic)
    return result

 