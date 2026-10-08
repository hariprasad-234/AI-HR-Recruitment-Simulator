import { useEffect, useState } from "react"
import { apiRequest } from "../Services/apiClient"

const DUMMY_CANDIDATES = [
  { id: 1, name: "Aarav Sharma", role: "Frontend Developer", score: 92, technical: 90, communication: 88, confidence: 95, skills: ["React", "Tailwind", "JavaScript"], experience: 3 },
  { id: 2, name: "Priya Nair", role: "Backend Developer", score: 87, technical: 91, communication: 80, confidence: 89, skills: ["Python", "FastAPI", "SQL"], experience: 4 },
  { id: 3, name: "Rohan Mehta", role: "Frontend Developer", score: 78, technical: 75, communication: 82, confidence: 76, skills: ["React", "CSS"], experience: 1 },
  { id: 4, name: "Sneha Iyer", role: "AI Engineer", score: 95, technical: 97, communication: 90, confidence: 96, skills: ["Python", "LangChain", "NLP"], experience: 5 },
  { id: 5, name: "Karan Verma", role: "Backend Developer", score: 65, technical: 60, communication: 70, confidence: 64, skills: ["Node.js", "MongoDB"], experience: 2 },
]

function Ranking() {
  const [candidates, setCandidates] = useState([])

  useEffect(() => {
    apiRequest("/api/candidates").then(setCandidates).catch(() => setCandidates(DUMMY_CANDIDATES))
  }, [])
  const [skillFilter, setSkillFilter] = useState("")
  const [minExperience, setMinExperience] = useState("")
  const [minScore, setMinScore] = useState("")
  const [expandedId, setExpandedId] = useState(null)
  const [compareMode, setCompareMode] = useState(false)
  const [selectedForCompare, setSelectedForCompare] = useState([])

  // FILTER + SORT LOGIC
  const filteredCandidates = candidates
    .filter((c) =>
      skillFilter
        ? c.skills.some((s) => s.toLowerCase().includes(skillFilter.toLowerCase()))
        : true
    )
    .filter((c) => (minExperience ? c.experience >= Number(minExperience) : true))
    .filter((c) => (minScore ? c.score >= Number(minScore) : true))
    .sort((a, b) => b.score - a.score)

  const toggleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id)
  }

  const toggleCompareSelect = (id) => {
    if (selectedForCompare.includes(id)) {
      setSelectedForCompare(selectedForCompare.filter((c) => c !== id))
    } else if (selectedForCompare.length < 3) {
      setSelectedForCompare([...selectedForCompare, id])
    }
  }

  const handleExportCSV = () => {
    const headers = ["Name", "Role", "Score", "Technical", "Communication", "Confidence", "Experience", "Skills"]
    const rows = filteredCandidates.map((c) => [
      c.name, c.role, c.score, c.technical, c.communication, c.confidence, c.experience, c.skills.join("; "),
    ])

    const csvContent = [headers, ...rows].map((row) => row.join(",")).join("\n")
    const blob = new Blob([csvContent], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = "candidate_rankings.csv"
    link.click()
    URL.revokeObjectURL(url)
  }

  const compareList = candidates.filter((c) => selectedForCompare.includes(c.id))

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-6xl mx-auto">

        <h1 className="text-3xl font-bold text-gray-800">Recruiter Dashboard</h1>
        <p className="mt-1 text-gray-500">Candidate ranking sorted by AI score</p>

        {/* FILTERS */}
        <div className="mt-6 flex flex-wrap gap-4 rounded-xl bg-white p-4 shadow">
          <input
            type="text"
            placeholder="Filter by skill (e.g. React)"
            value={skillFilter}
            onChange={(e) => setSkillFilter(e.target.value)}
            className="rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none"
          />

          <input
            type="number"
            placeholder="Min experience (years)"
            value={minExperience}
            onChange={(e) => setMinExperience(e.target.value)}
            className="rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none"
          />

          <input
            type="number"
            placeholder="Min score"
            value={minScore}
            onChange={(e) => setMinScore(e.target.value)}
            className="rounded-lg border border-gray-300 px-4 py-2 focus:border-blue-500 focus:outline-none"
          />

          <button
            onClick={() => setCompareMode(!compareMode)}
            className={`rounded-lg px-4 py-2 font-semibold ${
              compareMode ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-700"
            }`}
          >
            {compareMode ? "Exit Compare Mode" : "Compare Candidates"}
          </button>

          <button
            onClick={handleExportCSV}
            className="rounded-lg bg-green-600 px-4 py-2 font-semibold text-white hover:bg-green-700"
          >
            Export CSV
          </button>
        </div>

        {/* COMPARE VIEW */}
        {compareMode && compareList.length > 0 && (
          <div className="mt-6 rounded-xl bg-white p-4 shadow">
            <h2 className="text-lg font-bold text-gray-800">Comparing {compareList.length} Candidates</h2>
            <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              {compareList.map((c) => (
                <div key={c.id} className="rounded-lg border border-gray-200 p-4">
                  <h3 className="font-semibold text-gray-800">{c.name}</h3>
                  <p className="text-sm text-gray-500">{c.role}</p>
                  <p className="mt-2 text-2xl font-bold text-blue-600">{c.score}</p>
                  <div className="mt-2 text-sm text-gray-600 space-y-1">
                    <p>Technical: {c.technical}</p>
                    <p>Communication: {c.communication}</p>
                    <p>Confidence: {c.confidence}</p>
                    <p>Experience: {c.experience} yrs</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* CANDIDATE TABLE */}
        <div className="mt-6 overflow-x-auto rounded-xl bg-white shadow">
          <table className="w-full text-left">
            <thead className="bg-gray-50 text-sm text-gray-600">
              <tr>
                {compareMode && <th className="px-4 py-3"></th>}
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3">Score</th>
                <th className="px-4 py-3">Experience</th>
                <th className="px-4 py-3">Skills</th>
              </tr>
            </thead>
            <tbody>
              {filteredCandidates.map((c) => (
                <>
                  <tr
                    key={c.id}
                    onClick={() => !compareMode && toggleExpand(c.id)}
                    className="border-t border-gray-100 hover:bg-gray-50 cursor-pointer"
                  >
                    {compareMode && (
                      <td className="px-4 py-3">
                        <input
                          type="checkbox"
                          checked={selectedForCompare.includes(c.id)}
                          onChange={() => toggleCompareSelect(c.id)}
                          onClick={(e) => e.stopPropagation()}
                        />
                      </td>
                    )}
                    <td className="px-4 py-3 font-medium text-gray-800">{c.name}</td>
                    <td className="px-4 py-3 text-gray-600">{c.role}</td>
                    <td className="px-4 py-3 font-semibold text-blue-600">{c.score}</td>
                    <td className="px-4 py-3 text-gray-600">{c.experience} yrs</td>
                    <td className="px-4 py-3 text-gray-600">{c.skills.join(", ")}</td>
                  </tr>

                  {expandedId === c.id && !compareMode && (
                    <tr className="bg-gray-50">
                      <td colSpan={5} className="px-4 py-4">
                        <div className="grid grid-cols-3 gap-4 text-sm text-gray-700">
                          <div>
                            <p className="font-semibold">Technical</p>
                            <p>{c.technical}/100</p>
                          </div>
                          <div>
                            <p className="font-semibold">Communication</p>
                            <p>{c.communication}/100</p>
                          </div>
                          <div>
                            <p className="font-semibold">Confidence</p>
                            <p>{c.confidence}/100</p>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>

          {filteredCandidates.length === 0 && (
            <p className="p-6 text-center text-gray-500">No candidates match these filters.</p>
          )}
        </div>

      </div>
    </div>
  )
}

export default Ranking