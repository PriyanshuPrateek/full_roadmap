from llm_client import generate_topic_details
from cache_manager import get_cached_topic,save_topic

def generate_topic(topic: str):

    cached = get_cached_topic(topic)
    if cached:
        print("Returning topic from cache")
        return cached

    topic_data = generate_topic_details(topic)

    save_topic(topic, topic_data)

    return topic_data