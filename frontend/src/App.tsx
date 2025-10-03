import { useState } from "react";

type Message = { role: "user" | "bot"; text: string };

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages((msgs) => [...msgs, { role: "user", text: input }]);
    setLoading(true);

    try {
      const res = await fetch(`http://localhost:8002/rag/summary?topic=${encodeURIComponent(input)}`);
      const data = await res.json();
      let botText = data.summary;
      //if (data.papers && Array.isArray(data.papers) && data.papers.length > 0) {
      //  botText += "\n\nPapers:\n" + data.papers.map((p: any) => `- ${p.title}`).join("\n");
      //}
      setMessages((msgs) => [...msgs, { role: "bot", text: botText }]);
    } catch (err) {
      setMessages((msgs) => [...msgs, { role: "bot", text: "Error: Could not get response." }]);
    }
    setLoading(false);
    setInput("");
  };

  // Initial layout before any messages
  if (messages.length === 0 && !loading) {
    return (
      <div className="min-h-screen w-screen bg-neutral-900 flex flex-col justify-center items-center">
        <h1 className="text-7xl font-bold text-gray-100 text-center mb-2">Scholar Snap</h1>
        <h2 className="text-4xl text-gray-400 mb-8 text-center">Your Weekly Preprint Digest</h2>

        <div className="w-full max-w-6xl px-4">
          <form className="flex items-center bg-neutral-800 rounded-full shadow-lg px-6 py-4" onSubmit={handleSubmit}>
            <input
              type="text"
              className="flex-1 bg-transparent text-gray-100 placeholder-gray-400 outline-none border-none"
              placeholder="Type your scientific research topic of interest..."
              value={input}
              onChange={e => setInput(e.target.value)}
            />
            <button
              type="submit"
              disabled={!input.trim()}
              className={`ml-4 rounded-full p-2 transition-colors ${
                input.trim()
                  ? "bg-white text-neutral-900 hover:bg-gray-200"
                  : "bg-gray-700 text-gray-400 cursor-not-allowed"
              }`}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 -rotate-90"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    );
  }

  // ChatGPT-like chat layout after first message
  return (
    <div className="min-h-screen w-screen bg-neutral-900 flex flex-col items-center py-8">
      <div className="w-full max-w-6xl px-4 flex flex-col h-[80vh]">
        <div className="flex-1 overflow-y-auto bg-neutral-800 rounded-lg shadow-lg p-6 mb-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex mb-6 ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              {msg.role === "bot" && (
                <div className="flex items-end mr-2">
                  <div className="w-8 h-8 rounded-full bg-green-600 flex items-center justify-center text-white font-bold">S</div>
                </div>
              )}
              <div
                className={`px-5 py-3 rounded-2xl max-w-[75%] whitespace-pre-line text-base shadow ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-100 text-gray-900 border border-gray-300"
                }`}
              >
                {msg.text}
              </div>
              {msg.role === "user" && (
                <div className="flex items-end ml-2">
                  <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">U</div>
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="flex mb-6 justify-start">
              <div className="w-8 h-8 rounded-full bg-green-600 flex items-center justify-center text-white font-bold mr-2">S</div>
              <div className="px-5 py-3 rounded-2xl max-w-[75%] bg-gray-100 text-gray-900 border border-gray-300 animate-pulse">...</div>
            </div>
          )}
        </div>
        <form className="flex items-center bg-neutral-800 rounded-full shadow-lg px-6 py-4" onSubmit={handleSubmit}>
          <input
            type="text"
            className="flex-1 bg-transparent text-gray-100 placeholder-gray-400 outline-none border-none"
            placeholder="Type your scientific research topic of interest..."
            value={input}
            onChange={e => setInput(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className={`ml-4 rounded-full p-2 transition-colors ${
              input.trim() && !loading
                ? "bg-white text-neutral-900 hover:bg-gray-200"
                : "bg-gray-700 text-gray-400 cursor-not-allowed"
            }`}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6 -rotate-90"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;