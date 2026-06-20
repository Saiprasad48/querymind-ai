import re
import sqlparse

FORBIDDEN_KEYWORDS = [
    "insert","update","delete","drop","alter","create","truncate",
    "grant","revoke","replace","merge","call","execute"
]

def clean_sql_query(sql: str) -> str:
    return sql.strip().rstrip(";").strip()

def is_read_only_query(sql: str) -> tuple[bool, str]:
    if not sql or not sql.strip():
        return False, "SQL query cannot be empty."
    cleaned_sql = clean_sql_query(sql)
    parsed = sqlparse.parse(cleaned_sql)
    if len(parsed) != 1:
        return False, "Only one SQL statement is allowed."
    statement = parsed[0]
    if statement.get_type() != "SELECT":
        return False, "Only SELECT queries are allowed."
    normalized_sql = cleaned_sql.lower()
    for keyword in FORBIDDEN_KEYWORDS:
        pattern = rf"\b{keyword}\b"
        if re.search(pattern, normalized_sql):
            return False, f"Forbidden SQL keyword detected: {keyword.upper()}"
    return True, "Query is safe."

def add_limit_if_missing(sql: str, limit: int = 100) -> str:
    cleaned_sql = clean_sql_query(sql)
    if re.search(r"\blimit\b", cleaned_sql, re.IGNORECASE):
        return cleaned_sql
    return f"{cleaned_sql} LIMIT {limit}"