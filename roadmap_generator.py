from llm_client import generate_llm_response
from retriever import retrieve, add_topics_bulk
from cache_manager import get_cached_roadmap,save_roadmap


def generate_roadmap(skill):

    cached = get_cached_roadmap(skill)
    if cached:
        print("Returning roadmap from cache")
        return cached

    context = retrieve(skill)

    roadmap = generate_llm_response(skill, context)

    topic_titles = [node["title"] for node in roadmap["nodes"]]
    add_topics_bulk(topic_titles)

    save_roadmap(skill,roadmap)

    return roadmap