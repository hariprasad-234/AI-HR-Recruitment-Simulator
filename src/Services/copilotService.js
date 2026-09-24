// src/services/copilotService.js
// API layer for the HR Copilot (Task 9).
//
// Expected FastAPI contract (share this with the backend/AI team):
//   POST {API_BASE}/api/copilot/query
//   body:     { query: string,
//               filters: { skills: string[], minScore: number|null, location: string|null },
//               history: [{ role: "user"|"assistant", content: string }] }
//   response: { reply: string,
//               candidates: [{ id, name, score, skills: string[], location, experience_years, summary }] }
//
// Set VITE_USE_MOCK=false in .env once the backend endpoint is live (Task 10 integration).

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const USE_MOCK = import.meta.env.VITE_USE_MOCK !== "false"; // mock by default

// ---------- Mock data (remove when backend is connected) ----------
const MOCK_CANDIDATES = [
  { id: 1, name: "Aarav Sharma", score: 94, skills: ["Python", "FastAPI", "SQL", "Machine Learning"], location: "Bangalore", experience_years: 4, summary: "Strong backend engineer with ML deployment experience." },
  { id: 2, name: "Priya Nair", score: 91, skills: ["Python", "Django", "AWS", "Docker"], location: "Remote", experience_years: 5, summary: "Full-stack Python developer, excellent communication." },
  { id: 3, name: "Rohan Mehta", score: 88, skills: ["React", "JavaScript", "Tailwind", "Node.js"], location: "Hyderabad", experience_years: 3, summary: "Frontend specialist with clean component architecture." },
  { id: 4, name: "Sneha Iyer", score: 86, skills: ["Python", "Machine Learning", "NLP", "SQL"], location: "Chennai", experience_years: 2, summary: "NLP researcher turned engineer; strong technical answers." },
  { id: 5, name: "Karthik Reddy", score: 82, skills: ["Java", "Spring Boot", "SQL", "Docker"], location: "Hyderabad", experience_years: 6, summary: "Reliable backend lead, confident in system design." },
  { id: 6, name: "Ananya Das", score: 79, skills: ["React", "TypeScript", "Figma"], location: "Remote", experience_years: 2, summary: "Detail-oriented UI developer with design sensibility." },
  { id: 7, name: "Vikram Singh", score: 75, skills: ["Python", "Flask", "PostgreSQL"], location: "Chennai", experience_years: 3, summary: "Solid fundamentals; communication needs polish." },
  { id: 8, name: "Meera Krishnan", score: 71, skills: ["Java", "Kotlin", "Android"], location: "Bangalore", experience_years: 4, summary: "Mobile developer exploring backend roles." },
];

const KNOWN_SKILLS = ["python", "react", "java", "sql", "docker", "aws", "nlp", "machine learning", "typescript", "node.js", "fastapi", "django"];

function mockReply({ query, filters }) {
  const q = query.toLowerCase();
  const topMatch = q.match(/top\s+(\d+)/);
  const limit = topMatch ? parseInt(topMatch[1], 10) : 5;
  const scoreMatch = q.match(/(?:above|over|>=?)\s*(\d{2})/);

  const skills = [
    ...new Set([...filters.skills.map((s) => s.toLowerCase()), ...KNOWN_SKILLS.filter((s) => q.includes(s))]),
  ];
  const minScore = scoreMatch ? parseInt(scoreMatch[1], 10) : filters.minScore ?? 0;
  const location =
    filters.location || ["bangalore", "chennai", "hyderabad", "remote"].find((l) => q.includes(l)) || null;

  const results = MOCK_CANDIDATES.filter(
    (c) =>
      c.score >= minScore &&
      (!location || c.location.toLowerCase() === location.toLowerCase()) &&
      skills.every((s) => c.skills.some((cs) => cs.toLowerCase() === s))
  )
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);

  if (!results.length) {
    return { reply: "I couldn't find candidates matching that. Try relaxing the score or skill filters.", candidates: [] };
  }
  return {
    reply: `Here ${results.length === 1 ? "is the best match" : `are the top ${results.length} matches`}, ranked by AI interview score. ${results[0].name} leads with ${results[0].score}%.`,
    candidates: results,
  };
}

// ---------- Real API ----------
export async function sendCopilotQuery({ query, filters, history = [], signal }) {
  if (USE_MOCK) {
    await new Promise((res) => setTimeout(res, 900));
    if (signal?.aborted) throw new DOMException("Aborted", "AbortError");
    return mockReply({ query, filters });
  }

  const token = localStorage.getItem("token"); // adjust key to match Task 2 (auth)
  const res = await fetch(`${API_BASE}/api/copilot/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...(token && { Authorization: `Bearer ${token}` }) },
    body: JSON.stringify({ query, filters, history }),
    signal,
  });

  if (!res.ok) {
    throw new Error(
      res.status === 401 ? "Session expired. Please log in again." : `Server error (${res.status}). Please try again.`
    );
  }
  const data = await res.json();
  return { reply: data.reply ?? "", candidates: data.candidates ?? [] };
}
