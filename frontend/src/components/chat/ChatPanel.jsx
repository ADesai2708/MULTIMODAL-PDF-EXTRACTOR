import { useState } from "react";
import api from "../../services/api";

function ChatPanel() {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {

    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      content: question
    };

    setMessages(prev => [...prev, userMessage]);

    try {

      setLoading(true);

      const response = await api.post("/query", {
        question
      });

      const assistantMessage = {
        role: "assistant",
        content: response.data.answer
      };

      setMessages(prev => [
        ...prev,
        assistantMessage
      ]);

      setImages(
        response.data.referenced_images || []
      );

      setQuestion("");

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);

    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 h-162.5 flex flex-col">

      <div className="p-4 border-b">
        <h2 className="font-semibold">
          Conversation
        </h2>
      </div>

      <div className="flex-1 overflow-auto p-4">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`
              mb-4
              p-3
              rounded-xl
              max-w-[85%]
              ${msg.role === "user"
                ? "bg-blue-600 text-white ml-auto"
                : "bg-slate-100"}
            `}
          >

            {msg.content}

          </div>

        ))}

        {loading && (
          <div className="bg-slate-100 p-3 rounded-xl w-fit">
            Thinking...
          </div>
        )}

      </div>

      <div className="p-4 border-t flex gap-2">

        <input
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Ask a question..."
          className="
            flex-1
            border
            rounded-lg
            p-3
            outline-none
          "
        />

        <button
          onClick={askQuestion}
          className="
            bg-blue-600
            text-white
            px-6
            rounded-lg
          "
        >
          Send
        </button>

      </div>

    </div>
  );
}

export default ChatPanel;