import { useState } from "react";
import axios from "axios";
import "./App.css";

type AskResponse = {
  question: string;
  sql: string;
  explanation: string;
  is_safe: boolean;
  safety_message: string;
  columns: string[];
  rows: Record<string, string | number | null>[];
  row_count: number;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
function App() {
  const [question, setQuestion] = useState(
    "Which product category generated the highest revenue?"
  );
  const [result, setResult] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const handleAskQuestion = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const response = await axios.post(`${API_BASE_URL}/ai/ask`, {
        question,
      });
      setResult(response.data);
    } catch (err: any) {
      console.error("API Error:", err);
      const detail = err.response?.data?.detail;
      if (typeof detail === "string") {
        setError(detail);
      } else if (detail?.message) {
        setError(detail.message);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError("Something went wrong while asking the AI assistant.");
      }
    } finally {
      setLoading(false);
    }
  };
  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">QueryMind AI</p>
        <h1>LLM-Powered SQL Data Analyst Assistant</h1>
        <p className="subtitle">
          Ask business questions in plain English. The assistant generates safe
          SQL, runs it on PostgreSQL, and returns the result.
        </p>
      </section>
      <section className="card">
        <label htmlFor="question">Ask a data question</label>
        <textarea
          id="question"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Example: Show total revenue by product category"
        />
        <button onClick={handleAskQuestion} disabled={loading}>
          {loading ? "Thinking..." : "Ask AI Assistant"}
        </button>
        {error && <div className="error">{error}</div>}
      </section>
      {result && (
        <section className="results">
          <div className="summary-grid">
            <div className="card">
              <h2>Explanation</h2>
              <p>{result.explanation}</p>
            </div>
            <div className="card">
              <h2>Safety Check</h2>
              <p>
                <strong>Status:</strong>{" "}
                {result.is_safe ? "Safe query" : "Unsafe query"}
              </p>
              <p>{result.safety_message}</p>
            </div>
          </div>
          <div className="card">
            <h2>Generated SQL</h2>
            <pre>{result.sql}</pre>
          </div>
          <div className="card">
            <h2>Results</h2>
            <p className="row-count">{result.row_count} row(s) returned</p>
            {result.rows.length > 0 ? (
              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      {result.columns.map((column) => (
                        <th key={column}>{column}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {result.rows.map((row, rowIndex) => (
                      <tr key={rowIndex}>
                        {result.columns.map((column) => (
                          <td key={column}>{row[column]}</td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p>No rows returned.</p>
            )}
          </div>
        </section>
      )}
    </main>
  );
}
export default App;