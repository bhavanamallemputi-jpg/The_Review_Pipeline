import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


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

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)