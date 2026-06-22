# QueryMind AI

QueryMind AI is a full-stack LLM-powered SQL Data Analyst Assistant that allows users to ask business questions in natural language, automatically generates safe PostgreSQL queries, executes them on a database, and returns results with explanations, charts, query history, and CSV export.

## Overview

Business users often need insights from databases but may not know SQL. QueryMind AI bridges that gap by converting plain English questions into safe SQL queries and presenting the results in a clean dashboard.

Example questions:

* Which product category generated the highest revenue?
* Show total revenue by region.
* Show monthly revenue trend.
* Which customers placed the most orders?
* Show total sales quantity by product category.

## Features

* Natural language to SQL generation using Gemini
* PostgreSQL database with sample sales data
* SQL safety validation before execution
* Read-only query execution
* Automatic result table generation
* Automatic chart visualization for numeric results
* Query history stored in PostgreSQL
* Delete and clear query history
* CSV export for result tables
* React + TypeScript frontend
* FastAPI backend
* Dockerized PostgreSQL setup

## Tech Stack

### Frontend

* React
* TypeScript
* Vite
* Axios
* Recharts
* CSS

### Backend

* FastAPI
* Python
* SQLAlchemy
* Pydantic
* Gemini API
* PostgreSQL
* Docker

### Database

* PostgreSQL
* Sample sales schema with customers, products, orders, and order items

## Architecture

```mermaid
flowchart TD
    A[User] --> B[React Frontend]
    B --> C[FastAPI Backend]
    C --> D[Gemini API]
    C --> E[SQL Safety Validator]
    E --> F[PostgreSQL Database]
    F --> C
    C --> G[Query History Storage]
    C --> B
    B --> H[Tables, Charts, CSV Export]
```

## How It Works

1. User enters a natural language question in the frontend.
2. The frontend sends the question to the FastAPI backend.
3. The backend reads the PostgreSQL schema.
4. Gemini generates a PostgreSQL SELECT query using the schema.
5. The SQL validator checks that the query is read-only and safe.
6. The backend executes the query on PostgreSQL.
7. Results are returned to the frontend.
8. The frontend displays the explanation, SQL, result table, and chart.
9. The query is saved in history for later reference.

## SQL Safety Guardrails

The backend blocks destructive SQL operations such as:

* INSERT
* UPDATE
* DELETE
* DROP
* ALTER
* CREATE
* TRUNCATE
* GRANT
* REVOKE
* EXECUTE

Only SELECT queries are allowed.

The backend also automatically adds a result limit if the generated query does not already include one.

## Project Structure

```text
querymind-ai/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── ai.py
│   │   │   ├── db.py
│   │   │   ├── history.py
│   │   │   └── query.py
│   │   │
│   │   ├── services/
│   │   │   ├── gemini_service.py
│   │   │   └── schema_service.py
│   │   │
│   │   ├── utils/
│   │   │   └── sql_validator.py
│   │   │
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── index.css
│   │
│   ├── package.json
│   └── .env.example
│
├── database/
│   └── init/
│       ├── 01_schema.sql
│       └── 02_query_history.sql
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

## API Endpoints

### Health

```text
GET /health
```

Checks if the backend is running.

### Database Health

```text
GET /db/health
```

Checks if PostgreSQL is connected.

### Database Schema

```text
GET /db/schema
```

Returns the database schema.

### Generate SQL

```text
POST /ai/generate-sql
```

Generates SQL from a natural language question.

Request:

```json
{
  "question": "Which product category generated the highest revenue?"
}
```

### Ask AI

```text
POST /ai/ask
```

Generates SQL, validates it, executes it, saves the query to history, and returns results.

Request:

```json
{
  "question": "Show total revenue by product category"
}
```

### Execute SQL

```text
POST /query/execute
```

Executes a safe read-only SQL query.

### Query History

```text
GET /history
DELETE /history
DELETE /history/{history_id}
```

Fetch, clear, or delete query history.

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd querymind-ai
```

### 2. Start PostgreSQL with Docker

```bash
docker compose up -d
```

### 3. Set up backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/querymind
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### 4. Set up frontend

```bash
cd frontend
npm install
```

Create a `.env` file inside `frontend/`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Run frontend:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Sample Questions

```text
Show total revenue by product category
```

```text
Which region generated the highest revenue?
```

```text
Show monthly revenue trend
```

```text
Which customers placed the most orders?
```

```text
Show total sales quantity by product category
```

## Current Limitations

* The app currently uses a sample sales database.
* Gemini-generated SQL is validated before execution, but complex analytical queries may still need improvement.
* Authentication is not yet implemented.
* Query history stores metadata but not full result snapshots.

## Future Improvements

* User authentication
* Upload CSV and create temporary tables
* Support multiple databases
* Better SQL evaluation and retry logic
* Role-based access control
* More advanced chart selection
* Query result caching
* Cloud deployment
* Dockerize frontend and backend
* Add unit and integration tests

## Author

Sai Prasad Reddy Kukudala
