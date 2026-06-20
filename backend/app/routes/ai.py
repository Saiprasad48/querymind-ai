from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.schema_service import get_schema_description
from app.services.gemini_service import generate_sql_from_question, GeminiServiceError
from app.utils.sql_validator import is_read_only_query
router = APIRouter(prefix="/ai", tags=["AI"])

class GenerateSQLRequest(BaseModel):
    question: str

@router.post("/generate-sql")
def generate_sql(request: GenerateSQLRequest):
    if not request.question or not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )
    try:
        schema_description = get_schema_description()
        generated_result = generate_sql_from_question(
            question=request.question,
            schema_description=schema_description
        )
        sql = generated_result["sql"]
        explanation = generated_result["explanation"]
        is_safe, safety_message = is_read_only_query(sql)
        return {
            "question": request.question,
            "sql": sql,
            "explanation": explanation,
            "is_safe": is_safe,
            "safety_message": safety_message
        }
    except GeminiServiceError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )