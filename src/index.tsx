import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import AskNyaiApp from "./App";
import reportWebVitals from "./reportWebVitals";

const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error(
    "Root element not found. Make sure you have <div id='root'></div> in your public/index.html"
  );
}

const root = ReactDOM.createRoot(rootElement);

root.render(
  <React.StrictMode>
    <AskNyaiApp />
  </React.StrictMode>
);

// Optional: measure performance
reportWebVitals();
