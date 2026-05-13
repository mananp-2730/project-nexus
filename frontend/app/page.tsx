"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [brief, setBrief] = useState("");
  const [budget, setBudget] = useState(10000);
  const [timeline, setTimeline] = useState(4);
  
  const [debate, setDebate] = useState<string[]>([]);
  const [visibleDebate, setVisibleDebate] = useState<string[]>([]);
  
  // NEW: State to hold our analytics data
  const [analytics, setAnalytics] = useState<{
    original_budget: number;
    final_cost: number;
    budget_saved: number;
  } | null>(null);

  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);

  const startWarRoom = async () => {
    if (!brief) return;
    setLoading(true);
    setDebate([]); 
    setVisibleDebate([]); 
    setAnalytics(null); // Clear old analytics

    try {
      // NOTE: If you are testing locally, use localhost:8000. 
      // If pushing to Vercel, change this back to your Render URL!
      const response = await fetch("http://localhost:8000/api/start-debate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          client_brief: brief,
          budget: budget,
          timeline_weeks: timeline
        }),
      });

      const data = await response.json();

      if (data.debate_log) {
        setDebate(data.debate_log);
        setIsTyping(true);
        // NEW: Save the analytics data if it exists!
        if (data.analytics) {
          setAnalytics(data.analytics);
        }
      } else {
        setVisibleDebate([`SYSTEM ERROR: Backend returned -> ${JSON.stringify(data)}`]);
      }
      
    } catch (error) {
      console.error("Error connecting to War Room:", error);
      setVisibleDebate(["SYSTEM ERROR: Could not connect to the Python backend."]);
    }

    setLoading(false);
  };

  useEffect(() => {
    if (isTyping && visibleDebate.length < debate.length) {
      const timer = setTimeout(() => {
        setVisibleDebate((prev) => [...prev, debate[prev.length]]);
      }, 1500); 
      return () => clearTimeout(timer); 
    } else if (visibleDebate.length === debate.length && debate.length > 0) {
      setIsTyping(false);
    }
  }, [debate, visibleDebate, isTyping]);

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">
        
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold tracking-tight text-blue-400">Project Nexus</h1>
          <p className="text-gray-400">AI Multi-Agent War Room</p>
        </div>

        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl space-y-6">
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-300">Client Brief & Core Concept</label>
            <textarea
              className="w-full bg-gray-800 border border-gray-700 rounded-lg p-4 text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
              rows={3}
              placeholder="e.g., I want a global ride-sharing app with 4k video streaming..."
              value={brief}
              onChange={(e) => setBrief(e.target.value)}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-300">Budget ($)</label>
              <input 
                type="number" 
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value))}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </div>
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-300">Timeline (Weeks)</label>
              <input 
                type="number" 
                value={timeline}
                onChange={(e) => setTimeline(Number(e.target.value))}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
              />
            </div>
          </div>

          <button
            onClick={startWarRoom}
            disabled={loading || isTyping}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-3 rounded-lg transition-colors flex justify-center items-center gap-2"
          >
            {loading ? (
              "Contacting Agents..."
            ) : isTyping ? (
              <span className="animate-pulse">Agents are debating...</span>
            ) : (
              "Initialize War Room Debate"
            )}
          </button>
        </div>

        {/* NEW: Analytics Dashboard Cards */}
        {analytics && !isTyping && (
          <div className="grid grid-cols-3 gap-4 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div className="bg-gray-800 p-5 rounded-xl border border-gray-700 text-center shadow-lg">
              <div className="text-sm text-gray-400 uppercase tracking-wider font-bold mb-1">Original Budget</div>
              <div className="text-3xl font-bold text-gray-200">${analytics.original_budget.toLocaleString()}</div>
            </div>
            <div className="bg-gray-800 p-5 rounded-xl border border-gray-700 text-center shadow-lg">
              <div className="text-sm text-gray-400 uppercase tracking-wider font-bold mb-1">Final MVP Cost</div>
              <div className="text-3xl font-bold text-blue-400">${analytics.final_cost.toLocaleString()}</div>
            </div>
            <div className="bg-green-900/20 p-5 rounded-xl border border-green-900/50 text-center shadow-lg">
              <div className="text-sm text-green-400 uppercase tracking-wider font-bold mb-1">Budget Saved</div>
              <div className="text-3xl font-bold text-green-400">${analytics.budget_saved.toLocaleString()}</div>
            </div>
          </div>
        )}

        {/* Debate Log */}
        {visibleDebate.length > 0 && (
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-800 shadow-xl space-y-4">
            <h2 className="text-xl font-bold text-gray-200 border-b border-gray-800 pb-2 flex justify-between items-center">
              <span>Debate Log</span>
              {isTyping && <span className="text-sm text-blue-400 animate-pulse">Typing...</span>}
            </h2>
            <div className="space-y-4">
              {visibleDebate.map((message, index) => {
                let colorClass = "text-gray-300 border-gray-700";
                let badge = "";
                
                if (message.startsWith("Sales:")) {
                  colorClass = "text-green-400 border-green-900/50 bg-green-900/10";
                  badge = "Sales";
                  message = message.replace("Sales: ", "");
                }
                if (message.startsWith("Engineering:")) {
                  colorClass = "text-red-400 border-red-900/50 bg-red-900/10";
                  badge = "Engineering";
                  message = message.replace("Engineering: ", "");
                }
                if (message.startsWith("Product Manager:")) {
                  colorClass = "text-purple-400 border-purple-900/50 bg-purple-900/10";
                  badge = "Product Manager";
                  message = message.replace("Product Manager: ", "");
                }
                if (message.startsWith("SYSTEM:")) {
                  colorClass = "text-yellow-400 border-yellow-900/50 font-mono text-sm";
                  badge = "🖥️ SYSTEM";
                  message = message.replace("SYSTEM: ", "");
                }

                return (
                  <div key={index} className={`p-5 rounded-lg border animate-in fade-in slide-in-from-bottom-2 duration-500 ${colorClass}`}>
                    <div className="font-bold text-sm mb-1 opacity-80">{badge}</div>
                    <div className="leading-relaxed whitespace-pre-wrap">{message}</div>
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