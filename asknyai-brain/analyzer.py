import os
from dotenv import load_dotenv
from rag_engine import retrieve_context
from openai import OpenAI

# Load environment variables from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

def ask_llm(question, context):
    prompt = f"""
You are AskNyai, a legal awareness assistant.
Given the following context from the Constitution or IPC, answer the user's question.

Context:
{context}

Question:
{question}

Answer (in simple, clear terms with section references if possible):
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def analyze_question(question):
    context = retrieve_context(question)
    reply = ask_llm(question, context)
    reply += "\n\nDisclaimer: This is not legal advice. AskNyai helps simplify law for awareness."
    return reply
