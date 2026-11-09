import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    raise ValueError("Groq API key not found")

client = Groq(api_key=api_key)


def review_code(source_code):

    prompt = f"""
    You are an expert Python and JavaScript code reviewer.

    Analyze the following source code and identify bugs.

    Classify bugs into:
    syntax, logic, security, performance, style.

    Assign severity:
    Low, Medium, High, Critical.

    Return a JSON object in this format:
    {{
        "bugs": [
            {{
                "line": 1,
                "type": "syntax",
                "severity": "High",
                "description": "Describe the issue"
            }}
        ]
    }}

    If no bugs are found, return:
    {{"bugs": []}}

    Return only valid JSON.

    Source code:
    {source_code}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )

    result = response.choices[0].message.content

    data = json.loads(result)

    return data.get("bugs", [])