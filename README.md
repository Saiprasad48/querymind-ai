# QueryMind AI

QueryMind AI is a full-stack LLM-powered SQL Data Analyst Assistant that allows users to ask business questions in natural language, generates safe PostgreSQL queries, executes them on a database, and returns results with explanations, tables, charts, query history, and CSV export.

## Live Demo

* Frontend: https://querymind-ai-umber.vercel.app
* Backend API Docs: https://querymind-ai-backend.onrender.com/docs

Note: The backend is hosted on Render’s free tier, so the first request may take some time if the service is waking up.

## Overview

Business users often need insights from databases but may not know SQL. QueryMind AI bridges that gap by converting plain English questions into safe SQL queries and displaying the results in a clean dashboard.

Example questions:

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

## Features

* Natural language to SQL generation using Gemini
* PostgreSQL database with sample sales data
* Safe read-only SQL validation
* Query execution through FastAPI
* Automatic result table generation
* Automatic chart visualization for numeric results
* Query history stored in PostgreSQL
* Delete and clear query history
* CSV export for query results
* Full-stack React dashboard
* Deployed frontend, backend, and database

## Tech Stack

### Frontend

* React
* TypeScript
* Vite
* Axios
* Recharts
* CSS
* Vercel

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Gemini API
* Render

### Database

* PostgreSQL
* Neon
* Docker PostgreSQL for local development

## Architecture

```mermaid
flowchart TD
    A[User] --> B[React Frontend on Vercel]
    B --> C[FastAPI Backend on Render]
    C --> D[Gemini API]
    C --> E[SQL Safety Validator]
    E --> F[Neon PostgreSQL Database]
    F --> C
    C --> G[Query History Storage]
    C --> B
    B --> H[Tables, Charts, CSV Export]
```

## How It Works

1. User enters a natural language business question in the React frontend.
2. The frontend sends the question to the FastAPI backend.
3. The backend reads the PostgreSQL schema.
4. Gemini generates a PostgreSQL `SELECT` query using the available schema.
5. The SQL safety validator checks that the query is read-only.
6. The backend executes the safe query on PostgreSQL.
7. Results are returned to the frontend.
8. The frontend displays the explanation, generated SQL, result table, and chart.
9. The question, generated SQL, explanation, row count, and timestamp are saved in query history.

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

Only `SELECT` queries are allowed.

If the generated query does not include a limit, the backend automatically adds a default result limit.

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

## Database Schema

The sample sales database contains:

### customers

Stores customer details such as customer name, region, and segment.

### products

Stores product name, category, and unit price.

### orders

Stores customer orders with order date and status.

### order_items

Stores products purchased in each order, including quantity and price.

### query_history

Stores user questions, generated SQL, explanations, row counts, and timestamps.

## API Endpoints

### Health Check

```http
GET /health
```

Checks if the backend is running.

### Database Health

```http
GET /db/health
```

Checks if PostgreSQL is connected.

### Database Schema

```http
GET /db/schema
```

Returns the available database schema.

### Generate SQL

```http
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

```http
POST /ai/ask
```

Generates SQL, validates it, executes it, stores the query in history, and returns the results.

Request:

```json
{
  "question": "Show total revenue by product category"
}
```

Example response:

```json
{
  "question": "Show total revenue by product category",
  "sql": "SELECT p.category, SUM(oi.quantity * oi.unit_price) AS total_revenue FROM order_items oi JOIN products p ON oi.product_id = p.product_id GROUP BY p.category ORDER BY total_revenue DESC LIMIT 100",
  "explanation": "This query calculates total revenue for each product category.",
  "is_safe": true,
  "safety_message": "Query is safe.",
  "columns": ["category", "total_revenue"],
  "rows": [
    {
      "category": "Furniture",
      "total_revenue": 3310
    }
  ],
  "row_count": 1,
  "history_id": 1
}
```

### Execute SQL

```http
POST /query/execute
```

Executes a safe read-only SQL query.

### Query History

```http
GET /history
```

Fetches recent query history.

```http
DELETE /history/{history_id}
```

Deletes a single history item.

```http
DELETE /history
```

Clears all query history.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Saiprasad48/querymind-ai.git
cd querymind-ai
```

### 2. Start PostgreSQL locally with Docker

```bash
docker compose up -d
```

This creates a local PostgreSQL database and loads the sample sales schema.

### 3. Set up the backend

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
ALLOWED_ORIGINS=http://localhost:5173
```

Run the backend:

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

### 4. Set up the frontend

Open a new terminal:

```bash
cd frontend
npm install
```

Create a `.env` file inside `frontend/`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Run the frontend:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

## Deployment

The project is deployed using free-tier friendly services:

| Layer    | Service         |
| -------- | --------------- |
| Frontend | Vercel          |
| Backend  | Render          |
| Database | Neon PostgreSQL |
| LLM      | Gemini API      |

### Frontend Deployment

The React frontend is deployed on Vercel.

Production frontend:

```text
https://querymind-ai-umber.vercel.app
```

Required Vercel environment variable:

```env
VITE_API_BASE_URL=https://querymind-ai-backend.onrender.com
```

### Backend Deployment

The FastAPI backend is deployed on Render.

Production backend API docs:

```text
https://querymind-ai-backend.onrender.com/docs
```

Required Render environment variables:

```env
DATABASE_URL=your_neon_postgresql_connection_string
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
ALLOWED_ORIGINS=http://localhost:5173,https://querymind-ai-umber.vercel.app
```

### Database Deployment

The production PostgreSQL database is hosted on Neon.

The following SQL files are used to initialize the database:

```text
database/init/01_schema.sql
database/init/02_query_history.sql
```

## Sample Questions to Try

```text
Show total revenue by product category
```

```text
Which product category generated the highest revenue?
```

```text
Show total revenue by region
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

```text
Show revenue by customer segment
```

## Current Limitations

* The app currently uses a sample sales database.
* The backend supports safe read-only SQL execution only.
* Complex analytical questions may require better prompt refinement.
* Authentication is not implemented yet.
* Query history stores metadata but not full result snapshots.
* Render free tier may cause a cold start delay.

## Future Improvements

* User authentication
* Upload CSV files and create temporary analysis tables
* Support multiple databases
* Add SQL retry and correction logic
* Add role-based access control
* Improve automatic chart selection
* Add query result caching
* Add unit and integration tests
* Dockerize frontend and backend
* Add full production monitoring

## Author

Sai Prasad Reddy Kukudala
