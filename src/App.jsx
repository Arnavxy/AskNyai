// src/App.jsx
import React, { useState } from "react";
import "./App.css";

export default function AskNyaiApp() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setResponse(null);

    try {
      const res = await fetch("https://asknyai.onrender.com/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          platform: "web",
          user: "webuser",
          message: query,
        }),
      });
      const data = await res.json();
      setResponse(data.reply);
    } catch (err) {
      setResponse("Sorry, something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <img src="/asknyai-logo.jpg" alt="AskNyai Logo" className="logo" />
      <h1>AskNyai – Indian Legal Q&A</h1>
      <p className="subtext">
        Ask questions about Indian law and get answers powered by The Indian
        Constitution and the Bharatiya Nyaya Sanhita.
      </p>

      <textarea
        className="input-box"
        placeholder="What is the punishment for theft under BNS?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      ></textarea>

      <button onClick={handleSubmit} className="ask-button">
        {loading ? "Analyzing..." : "Ask"}
      </button>

      {response && <div className="response-box">{response}</div>}
    </div>
  );
}
