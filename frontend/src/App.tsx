import { useEffect, useState } from "react";
import axios from "axios";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
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
  history_id: number | null;
};
type HistoryItem = {
  history_id: number;
  question: string;
  generated_sql: string;
  explanation: string;
  row_count: number;
  created_at: string;
};
type HistoryResponse = {
  history: HistoryItem[];
};
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
function isNumericValue(value: string | number | null) {
  if (value === null || value === "") return false;
  return !Number.isNaN(Number(value));
}
function getChartData(result: AskResponse | null) {
  if (!result || result.rows.length === 0) return null;
  const numericColumn = result.columns.find((column) =>
    result.rows.some((row) => isNumericValue(row[column]))
  );
  if (!numericColumn) return null;
  const labelColumn =
    result.columns.find((column) => column !== numericColumn) || numericColumn;
  const data = result.rows
    .map((row) => ({
      name: String(row[labelColumn]),
      value: Number(row[numericColumn]),
    }))
    .filter((item) => !Number.isNaN(item.value));
  if (data.length === 0) return null;
  return {
    labelColumn,
    numericColumn,
    data,
  };
}
function App() {
  const [question, setQuestion] = useState(
    "Which product category generated the highest revenue?"
  );
  const [result, setResult] = useState<AskResponse | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [error, setError] = useState("");
  const chartConfig = getChartData(result);
  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const response = await axios.get<HistoryResponse>(
        `${API_BASE_URL}/history?limit=10`
      );
      setHistory(response.data.history);
    } catch (err) {
      console.error("Failed to fetch history:", err);
    } finally {
      setHistoryLoading(false);
    }
  };
  useEffect(() => {
    fetchHistory();
  }, []);
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
      fetchHistory();
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
  const handleUseHistoryQuestion = (historyItem: HistoryItem) => {
    setQuestion(historyItem.question);
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };
  return (
    <main className="app">
      <section className="hero">
        <div>
          <p className="eyebrow">QueryMind AI</p>
          <h1>LLM-Powered SQL Data Analyst Assistant</h1>
          <p className="subtitle">
            Ask business questions in plain English. The assistant generates
            safe SQL, runs it on PostgreSQL, and returns the result.
          </p>
        </div>
        <div className="hero-panel">
          <p>Natural language</p>
          <span>→</span>
          <p>Safe SQL</p>
          <span>→</span>
          <p>Insights</p>
        </div>
      </section>
      <section className="workspace-grid">
        <div className="card question-card">
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
        </div>
        <aside className="card history-card">
          <div className="history-header">
            <h2>Recent Questions</h2>
            <button className="ghost-button" onClick={fetchHistory}>
              Refresh
            </button>
          </div>
          {historyLoading ? (
            <p className="row-count">Loading history...</p>
          ) : history.length > 0 ? (
            <div className="history-list">
              {history.map((item) => (
                <button
                  key={item.history_id}
                  className="history-item"
                  onClick={() => handleUseHistoryQuestion(item)}
                >
                  <span>{item.question}</span>
                  <small>
                    {item.row_count} row(s) •{" "}
                    {new Date(item.created_at).toLocaleString()}
                  </small>
                </button>
              ))}
            </div>
          ) : (
            <p className="row-count">No history yet. Ask your first question.</p>
          )}
        </aside>
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

              {result.history_id && (
                <p className="row-count">Saved as history #{result.history_id}</p>
              )}
            </div>
          </div>
          <div className="content-grid">
            <div className="card">
              <h2>Generated SQL</h2>
              <pre>{result.sql}</pre>
            </div>
            {chartConfig && (
              <div className="card">
                <h2>Visualization</h2>
                <p className="row-count">
                  Showing {chartConfig.numericColumn} by{" "}
                  {chartConfig.labelColumn}
                </p>
                <div className="chart-wrapper">
                  <ResponsiveContainer width="100%" height={320}>
                    <BarChart data={chartConfig.data}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="value" fill="#2563eb" radius={[8, 8, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}
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