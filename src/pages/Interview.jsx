import { useState, useEffect, useRef } from "react"
import { useParams } from "react-router-dom"

const DUMMY_QUESTIONS = [
  "Tell me about yourself and your experience.",
  "What is your biggest strength as a developer?",
  "Describe a challenging bug you fixed recently.",
  "How do you handle tight deadlines?",
]

function Interview() {
  const { candidateId } = useParams()

  const [messages, setMessages] = useState([
    { sender: "ai", text: DUMMY_QUESTIONS[0] },
  ])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [answer, setAnswer] = useState("")
  const [timeLeft, setTimeLeft] = useState(60)
  const [isComplete, setIsComplete] = useState(false)

  const chatEndRef = useRef(null)

  // AUTO SCROLL TO LATEST MESSAGE
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  // COUNTDOWN TIMER PER QUESTION
  useEffect(() => {
    if (isComplete) return

    if (timeLeft === 0) {
      handleSend()
      return
    }

    const timer = setTimeout(() => setTimeLeft((t) => t - 1), 1000)
    return () => clearTimeout(timer)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeLeft, isComplete])

  const handleSend = () => {
    const newMessages = [
      ...messages,
      { sender: "candidate", text: answer || "(No answer)" },
    ]

    const nextIndex = currentIndex + 1

    if (nextIndex < DUMMY_QUESTIONS.length) {
      newMessages.push({ sender: "ai", text: DUMMY_QUESTIONS[nextIndex] })
      setCurrentIndex(nextIndex)
      setTimeLeft(60)
    } else {
      setIsComplete(true)
    }

    setMessages(newMessages)
    setAnswer("")
  }

  // INTERVIEW COMPLETE SCREEN
  if (isComplete) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="w-full max-w-md rounded-xl bg-white p-8 shadow-lg text-center">
          <h1 className="text-3xl font-bold text-gray-800">
            Interview Complete 🎉
          </h1>
          <p className="mt-4 text-gray-500">
            Thank you! Your responses have been submitted for evaluation.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-2xl rounded-xl bg-white shadow-lg flex flex-col h-[80vh]">

        {/* HEADER */}
        <div className="flex items-center justify-between border-b border-gray-200 p-4">
          <span className="font-semibold text-gray-700">
            Question {currentIndex + 1} of {DUMMY_QUESTIONS.length}
          </span>
          <span className="font-mono text-sm text-red-500">
            {timeLeft}s
          </span>
        </div>

        {/* CHAT WINDOW */}
        <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`max-w-[75%] rounded-2xl px-4 py-2 text-sm ${
                msg.sender === "ai"
                  ? "self-start bg-gray-100 text-gray-800"
                  : "self-end bg-blue-600 text-white"
              }`}
            >
              {msg.text}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* INPUT AREA */}
        <div className="flex items-center gap-2 border-t border-gray-200 p-4">
          <input
            type="text"
            placeholder="Type your answer..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            className="flex-1 rounded-lg border border-gray-300 px-4 py-3 focus:border-blue-500 focus:outline-none"
          />

          <button
            onClick={handleSend}
            className="rounded-lg bg-blue-600 px-6 py-3 font-semibold text-white hover:bg-blue-700"
          >
            Send
          </button>
        </div>

      </div>
    </div>
  )
}

export default Interview