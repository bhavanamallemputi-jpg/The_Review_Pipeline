import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found in .env file")

client = genai.Client(api_key=api_key)


def review_code(source_code):

    prompt = f"""
    You are an expert Python and JavaScript code reviewer.

    Analyze the following source code and identify bugs.

    Classify bugs into:
    syntax, logic, security, performance, style.

    Assign severity:
    Low, Medium, High, Critical.

    Return a JSON array with:
    line, type, severity, description.

    If no bugs are found, return an empty array.

    Source code:
    {source_code}
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)