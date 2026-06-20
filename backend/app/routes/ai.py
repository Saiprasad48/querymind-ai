from typing import Any
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine
from app.services.schema_service import get_schema_description
from app.services.gemini_service import generate_sql_from_question, GeminiServiceError
from app.utils.sql_validator import is_read_only_query, add_limit_if_missing

router = APIRouter(prefix="/ai", tags=["AI"])
class GenerateSQLRequest(BaseModel):
    question: str
class AskQuestionRequest(BaseModel):
    question: str
class AskQuestionResponse(BaseModel):
    question: str
    sql: str
    explanation: str
    is_safe: bool
    safety_message: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int

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

@router.post("/ask", response_model=AskQuestionResponse)
def ask_question(request: AskQuestionRequest):
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
        if not is_safe:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Generated SQL failed safety validation.",
                    "sql": sql,
                    "safety_message": safety_message
                }
            )
        safe_sql = add_limit_if_missing(sql)
        with engine.connect() as connection:
            result = connection.execute(text(safe_sql))
            rows = [dict(row._mapping) for row in result.fetchall()]
            columns = list(result.keys())
        response = {
            "question": request.question,
            "sql": safe_sql,
            "explanation": explanation,
            "is_safe": is_safe,
            "safety_message": safety_message,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }
        return jsonable_encoder(response)
    except GeminiServiceError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail=f"SQL execution failed: {str(error)}"
        )