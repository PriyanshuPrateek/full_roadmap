import json
import os

ROADMAP_FILE = "cache/roadmap.json"
TOPIC_FILE = "cache/topic.json"


def _load(file_path):
    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as f:
        return json.load(f)


def _save(file_path, data):
    os.makedirs("cache", exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


# ROADMAP CACHE
def get_cached_roadmap(skill: str):
    data = _load(ROADMAP_FILE)
    return data.get(skill)

def save_roadmap(skill: str, roadmap: dict):
    data = _load(ROADMAP_FILE)
    data[skill] = roadmap
    _save(ROADMAP_FILE, data)

# TOPIC CACHE
def get_cached_topic(topic: str):
    data = _load(TOPIC_FILE)
    return data.get(topic)

def save_topic(topic: str, topic_data: dict):
    data = _load(TOPIC_FILE)
    data[topic] = topic_data
    _save(TOPIC_FILE, data)