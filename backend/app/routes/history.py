from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine

router = APIRouter(prefix="/history", tags=["History"])

@router.get("")
def get_query_history(limit: int = Query(default=20, ge=1, le=100)):
    try:
        query = text("""
            SELECT
                history_id,
                question,
                generated_sql,
                explanation,
                row_count,
                created_at
            FROM query_history
            ORDER BY created_at DESC
            LIMIT :limit;
        """)
        with engine.connect() as connection:
            rows = connection.execute(query, {"limit": limit}).mappings().all()
        history = [dict(row) for row in rows]
        return jsonable_encoder({
            "history": history
        })
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch query history: {str(error)}"
        )

@router.get("/{history_id}")
def get_query_history_item(history_id: int):
    try:
        query = text("""
            SELECT
                history_id,
                question,
                generated_sql,
                explanation,
                row_count,
                created_at
            FROM query_history
            WHERE history_id = :history_id;
        """)
        with engine.connect() as connection:
            row = connection.execute(
                query,
                {"history_id": history_id}
            ).mappings().first()
        if not row:
            raise HTTPException(
                status_code=404,
                detail="History item not found."
            )
        return jsonable_encoder(dict(row))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch history item: {str(error)}"
        )