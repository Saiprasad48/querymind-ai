from sqlalchemy import text
from app.database import engine

def get_schema_description() -> str:
    query = text("""
        SELECT 
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name NOT IN ('query_history')
        ORDER BY table_name, ordinal_position;
    """)
    schema = {}
    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()
    for row in rows:
        table_name = row["table_name"]
        if table_name not in schema:
            schema[table_name] = []
        schema[table_name].append(
            f"{row['column_name']} {row['data_type']}"
        )
    schema_lines = []
    for table_name, columns in schema.items():
        schema_lines.append(
            f"Table: {table_name}\nColumns: {', '.join(columns)}"
        )
    return "\n\n".join(schema_lines)