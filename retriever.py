from embedding import generate_embedding
from vectordb import VectorStore

vector_store = VectorStore()

def retrieve(skill: str, k=5):
    """
    Retrieve semantically similar topics from vector database
    """
    embedding = generate_embedding(skill)
    results = vector_store.search(embedding, k)
    return results

def add_topic(topic: str):
    """
    Add new topic dynamically to vector database
    """
    embedding = generate_embedding(topic)
    vector_store.add(embedding, topic)

def add_topics_bulk(topics: list):
    """
    Add multiple topics
    """
    for topic in topics:
        add_topic(topic)