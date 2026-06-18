from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine

router = APIRouter(prefix="/db", tags=["Database"])

@router.get("/health")
def database_health():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()
        return {
            "database": "connected",
            "test_query_result": result
        }
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(error)}"
        )

@router.get("/schema")
def get_database_schema():
    try:
        query = text("""
            SELECT 
                table_name,
                column_name,
                data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """)
        schema = {}
        with engine.connect() as connection:
            rows = connection.execute(query).mappings().all()
        for row in rows:
            table_name = row["table_name"]
            if table_name not in schema:
                schema[table_name] = []
            schema[table_name].append({
                "column_name": row["column_name"],
                "data_type": row["data_type"]
            })
        return {
            "tables": schema
        }
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch schema: {str(error)}"
        )