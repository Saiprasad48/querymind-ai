import json
import re
from google import genai
from app.config import settings

class GeminiServiceError(Exception):
    pass

def extract_json_from_text(text: str) -> dict:
    """
    Gemini may sometimes return JSON inside markdown fences.
    This function safely extracts the JSON object.
    """
    cleaned_text = text.strip()
    cleaned_text = re.sub(r"^```json", "", cleaned_text)
    cleaned_text = re.sub(r"^```", "", cleaned_text)
    cleaned_text = re.sub(r"```$", "", cleaned_text)
    cleaned_text = cleaned_text.strip()
    start = cleaned_text.find("{")
    end = cleaned_text.rfind("}")
    if start == -1 or end == -1:
        raise GeminiServiceError("Gemini did not return valid JSON.")
    json_text = cleaned_text[start:end + 1]
    try:
        return json.loads(json_text)
    except json.JSONDecodeError:
        raise GeminiServiceError("Failed to parse Gemini JSON response.")

def generate_sql_from_question(question: str, schema_description: str) -> dict:
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_real_gemini_api_key_here":
        raise GeminiServiceError("GEMINI_API_KEY is not configured.")
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    prompt = f"""
You are an expert PostgreSQL data analyst.
Convert the user's natural language question into a safe PostgreSQL SELECT query.

Rules:
- Use only the provided database schema.
- Generate only SELECT queries.
- Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, or destructive SQL.
- Do not guess table names or column names.
- Use readable aliases when helpful.
- Return only valid JSON.
- Do not wrap the JSON in markdown.

Return JSON in this exact format:
{{
  "sql": "SELECT ...",
  "explanation": "Short explanation of what the SQL does."
}}

Database schema:
{schema_description}

User question:
{question}
"""

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )
        if not response.text:
            raise GeminiServiceError("Gemini returned an empty response.")
        result = extract_json_from_text(response.text)
        if "sql" not in result or "explanation" not in result:
            raise GeminiServiceError("Gemini response is missing required fields.")
        return result
    except GeminiServiceError:
        raise
    except Exception as error:
        raise GeminiServiceError(f"Failed to generate SQL with Gemini: {str(error)}")