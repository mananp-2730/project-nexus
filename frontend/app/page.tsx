"use client";

import { useState } from "react";

export default function Home() {
  const [brief, setBrief] = useState("");
  const [debate, setDebate] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const startWarRoom = async () => {
    if (!brief) return;
    setLoading(true);
    setDebate([]); // Clear old debate

    try {
      // Talk to our Python Backend!
      const response = await fetch("http://127.0.0.1:8000/api/start-debate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ client_brief: brief }),
      });

      const data = await response.json();
      setDebate(data.debate_log);
    } catch (error) {
      console.error("Error connecting to War Room:", error);
      setDebate(["SYSTEM ERROR: Could not connect to the Python backend."]);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight text-blue-400">Project Nexus</h1>
          <p className="text-gray-400">AI Multi-Agent War Room</p>
        </div>

        {/* Input Section */}
        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl space-y-4">
          <label className="block text-sm font-medium text-gray-300">Enter Client Brief & Constraints</label>
          <textarea
            className="w-full bg-gray-800 border border-gray-700 rounded-lg p-4 text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
            rows={4}
            placeholder="e.g., I want a global ride-sharing app with 4k video streaming. Budget: $10k."
            value={brief}
            onChange={(e) => setBrief(e.target.value)}
          />
          <button
            onClick={startWarRoom}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-3 rounded-lg transition-colors"
          >
            {loading ? "Agents are arguing..." : "Initialize War Room Debate"}
          </button>
        </div>

        {/* Debate Log Section */}
        {debate.length > 0 && (
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl space-y-4">
            <h2 className="text-xl font-bold text-gray-200 border-b border-gray-800 pb-2">Debate Log</h2>
            <div className="space-y-4">
              {debate.map((message, index) => {
                // Quick color coding based on who is speaking
                let colorClass = "text-gray-300";
                if (message.startsWith("Sales:")) colorClass = "text-green-400";
                if (message.startsWith("Engineering:")) colorClass = "text-red-400";
                if (message.startsWith("Product Manager:")) colorClass = "text-purple-400";
                if (message.startsWith("SYSTEM:")) colorClass = "text-yellow-400 font-mono text-sm";

                return (
                  <div key={index} className={`p-4 bg-gray-800 rounded-lg border border-gray-700 ${colorClass}`}>
                    {message}
                  </div>
                );
              })}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}