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


def refactor_code(source_code):

    prompt = f"""
    You are an expert Python code refactoring assistant.

    Improve the following code.

    Requirements:
    1. Improve readability.
    2. Improve variable names.
    3. Remove unnecessary code.
    4. Improve code structure.
    5. Do not change the original functionality.

    Return a JSON object containing:
    refactored_code: The complete improved code.
    explanation: A short explanation of improvements.

    Original source code:
    {source_code}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
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

    return json.loads(result)