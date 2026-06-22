CREATE TABLE IF NOT EXISTS query_history (
    history_id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    generated_sql TEXT NOT NULL,
    explanation TEXT,
    row_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);