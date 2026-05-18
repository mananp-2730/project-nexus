"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [brief, setBrief] = useState("");
  const [budget, setBudget] = useState(10000);
  const [timeline, setTimeline] = useState(4);
  
  const [debate, setDebate] = useState<string[]>([]);
  const [visibleDebate, setVisibleDebate] = useState<string[]>([]);
  
  const [analytics, setAnalytics] = useState<{
    original_budget: number;
    final_cost: number;
    budget_saved: number;
  } | null>(null);

  // NEW: State to hold our Supabase history
  const [history, setHistory] = useState<any[]>([]);

  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);

  // NEW: Fetch history from the backend
  const fetchHistory = async () => {
    try {
      // NOTE: Use localhost:8000 for local testing. Update to Render URL for production!
      const res = await fetch("http://localhost:8000/api/history");
      const data = await res.json();
      if (data.history) {
        setHistory(data.history);
      }
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };

  // NEW: Run fetchHistory exactly once when the app loads
  useEffect(() => {
    fetchHistory();
  }, []);

  const startWarRoom = async () => {
    if (!brief) return;
    setLoading(true);
    setDebate([]); 
    setVisibleDebate([]); 
    setAnalytics(null); 

    try {
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
        if (data.analytics) {
          setAnalytics(data.analytics);
        }
        // Refresh the sidebar to show the newly saved debate!
        fetchHistory();
      } else {
        setVisibleDebate([`SYSTEM ERROR: Backend returned -> ${JSON.stringify(data)}`]);
      }
      
    } catch (error) {
      console.error("Error connecting to War Room:", error);
      setVisibleDebate(["SYSTEM ERROR: Could not connect to the Python backend."]);
    }

    setLoading(false);
  };

  // NEW: Function to load a past debate from the sidebar into the main window
  const loadPastDebate = (pastDebate: any) => {
    setBrief(pastDebate.client_brief);
    setBudget(pastDebate.original_budget);
    setTimeline(pastDebate.timeline_weeks);
    setDebate(pastDebate.debate_log);
    setVisibleDebate(pastDebate.debate_log); // Show instantly without typing effect
    setAnalytics({
      original_budget: pastDebate.original_budget,
      final_cost: pastDebate.final_cost,
      budget_saved: pastDebate.budget_saved
    });
    setIsTyping(false);
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
    // NEW: Flex layout for the Sidebar
    <div className="flex h-screen bg-gray-950 text-white font-sans overflow-hidden">
      
      {/* --- SIDEBAR --- */}
      <div className="w-80 bg-gray-900 border-r border-gray-800 flex flex-col overflow-y-auto">
        <div className="p-6 border-b border-gray-800 sticky top-0 bg-gray-900 z-10">
          <h2 className="text-xl font-bold text-gray-200">Past War Rooms</h2>
          <p className="text-xs text-gray-500 mt-1">Click to review previous debates</p>
        </div>
        <div className="flex-1 p-4 space-y-3">
          {history.map((item) => (
            <button
              key={item.id}
              onClick={() => loadPastDebate(item)}
              className="w-full text-left bg-gray-800 hover:bg-gray-750 border border-gray-700 hover:border-blue-500 p-4 rounded-lg transition-all shadow-sm group"
            >
              <div className="text-sm font-semibold text-gray-300 line-clamp-2 mb-2 group-hover:text-blue-400">
                "{item.client_brief}"
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-gray-500">{new Date(item.created_at).toLocaleDateString()}</span>
                <span className="bg-green-900/30 text-green-400 px-2 py-1 rounded-md font-bold border border-green-900/50">
                  Saved ${item.budget_saved.toLocaleString()}
                </span>
              </div>
            </button>
          ))}
          {history.length === 0 && (
            <div className="text-center text-gray-600 text-sm py-8">
              No past debates found.
            </div>
          )}
        </div>
      </div>

      {/* --- MAIN CONTENT --- */}
      <div className="flex-1 overflow-y-auto p-8">
        <div className="max-w-4xl mx-auto space-y-8 pb-12">
          
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

          {/* Analytics Dashboard Cards */}
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
                    badge = "💼 Sales";
                    message = message.replace("Sales: ", "");
                  }
                  if (message.startsWith("Engineering:")) {
                    colorClass = "text-red-400 border-red-900/50 bg-red-900/10";
                    badge = "⚙️ Engineering";
                    message = message.replace("Engineering: ", "");
                  }
                  if (message.startsWith("Product Manager:")) {
                    colorClass = "text-purple-400 border-purple-900/50 bg-purple-900/10";
                    badge = "🎯 Product Manager";
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
    </div>
  );
}