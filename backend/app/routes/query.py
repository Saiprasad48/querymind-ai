from typing import Any
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine
from app.utils.sql_validator import is_read_only_query, add_limit_if_missing

router = APIRouter(prefix="/query", tags=["Query"])

class SQLQueryRequest(BaseModel):
    sql: str

class SQLQueryResponse(BaseModel):
    sql: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int

@router.post("/execute", response_model=SQLQueryResponse)
def execute_sql_query(request: SQLQueryRequest):
    is_safe, message = is_read_only_query(request.sql)
    if not is_safe:
        raise HTTPException(
            status_code=400,
            detail=message
        )
    safe_sql = add_limit_if_missing(request.sql)
    try:
        with engine.connect() as connection:
            result = connection.execute(text(safe_sql))
            rows = [dict(row._mapping) for row in result.fetchall()]
            columns = list(result.keys())
        response = {
            "sql": safe_sql,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }
        return jsonable_encoder(response)
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail=f"SQL execution failed: {str(error)}"
        )