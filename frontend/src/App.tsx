import { useState } from "react";

function App() {
  const [input, setInput] = useState("");

  return (
    <div className="min-h-screen w-screen bg-neutral-900 flex flex-col justify-center items-center">
      <h1 className="text-2xl font-medium text-gray-100 mb-8 text-center">
        Which scientific topic are you interested in?
      </h1>
      <div className="w-full max-w-2xl px-4">
        <form className="flex items-center bg-neutral-800 rounded-full shadow-lg px-6 py-4">
          <input
            type="text"
            className="flex-1 bg-transparent text-gray-100 placeholder-gray-400 outline-none border-none"
            placeholder="Ask anything"
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
            {/* Upward arrow icon (SVG, rotated) */}
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