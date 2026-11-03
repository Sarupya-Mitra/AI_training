import { useEffect, useState } from "react";
import "./App.css";

const API = "http://localhost:8000";

function App() {
  const [models, setModels] = useState([]);
  const [selected, setSelected] = useState([]);
  const [question, setQuestion] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API}/models`)
      .then(res => res.json())
      .then(setModels)
      .catch(console.error);
  }, []);

  function toggleModel(id) {
    setSelected(prev => {
      if (prev.includes(id)) {
        return prev.filter(m => m !== id);
      }

      if (prev.length >= 3) {
        alert("You can select up to 3 models.");
        return prev;
      }

      return [...prev, id];
    });
  }

  async function askModels() {
    if (!question.trim() || selected.length === 0) {
      return;
    }

    setLoading(true);
    setResults([]);

    try {
      const response = await fetch(`${API}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          question,
          models: selected
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Request failed");
      }

      setResults(data.results);

    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="container">

      <h1>RAG Model Arena</h1>
      <p>Compare answers from multiple LLMs.</p>

      <section>
        <h3>Enter your question</h3>

        <textarea
          value={question}
          onChange={e => setQuestion(e.target.value)}
          placeholder="Ask something about your documents..."
        />

        <h3>Select models (maximum 3)</h3>

        {models.map(model => (
          <label key={model.id} className="model-option">
            <input
              type="checkbox"
              checked={selected.includes(model.id)}
              onChange={() => toggleModel(model.id)}
            />

            {model.name}
          </label>
        ))}

        <p>{selected.length}/3 models selected</p>

        <button
          onClick={askModels}
          disabled={loading || !question.trim() || selected.length === 0}
        >
          {loading ? "Generating answers..." : "Compare Models"}
        </button>
      </section>

      {results.length > 0 && (
        <section>
          <h2>Model Responses</h2>

          <div className="results-grid">
            {results.map((result, index) => (
              <div className="result-card" key={index}>
                <h3>{result.actual_model || result.requested_model}</h3>

                {result.error ? (
                  <p className="error">{result.error}</p>
                ) : (
                  <p>{result.answer}</p>
                )}

                <hr />

                <p>
                  Response time: {result.response_time} seconds
                </p>

                <p>
                  Tokens: {result.tokens ?? "N/A"}
                </p>

                {/* <p>
                  Accuracy: {result.accuracy ?? "Not evaluated"}
                </p> */}
              </div>
            ))}
          </div>

          <h2>Performance Statistics</h2>

          <table>
            <thead>
              <tr>
                <th>Model</th>
                <th>Time (sec)</th>
                <th>Tokens</th>
                {/* <th>Accuracy</th> */}
              </tr>
            </thead>

            <tbody>
              {results.map((r, i) => (
                <tr key={i}>
                  <td>{r.actual_model || r.requested_model}</td>
                  <td>{r.response_time}</td>
                  <td>{r.tokens ?? "N/A"}</td>
                  {/* <td>{r.accuracy ?? "Pending"}</td> */}
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}

    </div>
  );
}

export default App;