import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from schema import Roadmap
import json
from topic_schema import TopicDetails
load_dotenv()


llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.2
)

parser = PydanticOutputParser(pydantic_object=Roadmap)


def generate_llm_response(skill: str, context: list = None) -> dict:
   

    format_instructions =  format_instructions = """
 Return output STRICTLY in this JSON format:

 {
  "nodes": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "estimated_hours": integer,
      "level": "Beginner | Intermediate | Advanced"
    }
  ],
  "edges": [
    {
      "source": "string",
      "target": "string"
    }
  ]
  }

 Return ONLY valid JSON. No schema. No explanations.
 """

    context_block = ""

    if context and len(context) > 0:
        context_block = f"""
    Relevant topics from knowledge base:
    {context}

    Use these topics if relevant. You may add additional topics if needed.
    """
        
    prompt = f"""
    You are an expert AI roadmap generator.

    Your task is to generate a COMPLETE and BALANCED learning roadmap for:

    Skill: {skill}

    {context_block}

    {format_instructions}

    CRITICAL STRUCTURE RULES:

    1. The roadmap MUST include ALL major conceptual branches.

    Example for Machine Learning:
    - Foundations
    - Data Preprocessing
    - Supervised Learning
    - Unsupervised Learning
    - Reinforcement Learning
    - Model Evaluation
    - Deep Learning
    - Deployment

    2. DO NOT over-expand a single concept.

    Example:
    If including "Supervised Learning", include it as ONE node.
    Do NOT list every algorithm like Linear Regression, Logistic Regression separately unless necessary.

    3. Focus on learning phases, NOT exhaustive algorithm lists.

    4. Each node should represent a meaningful learning stage.

    5. Roadmap must be concept-based, not algorithm-dump.

    6. Ensure balanced coverage across entire skill.

    7. Avoid going too deep into one branch while ignoring others.

    TIME RULES:

    - Beginner: 5–20 hours
    - Intermediate: 15–40 hours
    - Advanced: 20–60 hours
    - Maximum per topic: 60 hours

    OUTPUT RULES:

    - Return ONLY valid JSON
    - No explanations outside JSON
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    parsed_output = parser.parse(response.content)

    return parsed_output.model_dump()

par = PydanticOutputParser(pydantic_object=TopicDetails)
def generate_topic_details(topic: str) -> dict:

      format_instruction = """
      Return ONLY valid JSON:
     {
      "title": "{topic}",
      "description": "3–5 sentence explanation",
      "subtopics": ["Subtopic 1", "Subtopic 2"],
      "estimated_hours": integer
     }
    """
      prompt = f"""
    You are a senior curriculum designer and industry expert.
    Your task is to generate detailed and PRACTICAL learning information for:
    Topic: {topic}

    {format_instruction}

    CONTENT QUALITY RULES:
    - Provide a concise but clear technical description.
    - Subtopics must be logically ordered (basic → advanced).
    - Include 5–10 meaningful subtopics.
    - Subtopics must be specific.
    TIME ESTIMATION RULES:
    - Beginner topic: 5–20 hours
    - Intermediate topic: 15–40 hours
    - Advanced topic: 20–60 hours
    - NEVER exceed 60 hours.
    Return ONLY valid JSON:
    
    """
      response = llm.invoke([HumanMessage(content=prompt)])

      parsed_out = par.parse(response.content)

      return parsed_out.model_dump()