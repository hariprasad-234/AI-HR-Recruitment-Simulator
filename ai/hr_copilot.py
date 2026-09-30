import os
import json
from dotenv import load_dotenv
from google import genai


# ============================================================
# Environment Setup
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )

client = genai.Client(api_key=api_key)


# ============================================================
# Sample Candidate Data
# ============================================================

CANDIDATES = [
    {
        "candidate_id": "candidate_001",
        "name": "Candidate 1",
        "skills": [
            "Python",
            "Machine Learning",
            "TensorFlow",
            "PyTorch",
            "Computer Vision",
            "SQL",
            "Flask"
        ],
        "experience_years": 2,
        "match_score": 82,
        "interview_score": 84
    },
    {
        "candidate_id": "candidate_002",
        "name": "Candidate 2",
        "skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Scikit-learn"
        ],
        "experience_years": 1,
        "match_score": 74,
        "interview_score": 76
    },
    {
        "candidate_id": "candidate_003",
        "name": "Candidate 3",
        "skills": [
            "Java",
            "SQL",
            "Spring Boot",
            "React"
        ],
        "experience_years": 3,
        "match_score": 61,
        "interview_score": 68
    }
]


# ============================================================
# Candidate Search
# ============================================================

def search_candidates(
    skill=None,
    minimum_match_score=None,
    minimum_interview_score=None
):
    """
    Search candidates using structured recruitment criteria.
    """

    results = CANDIDATES

    if skill:
        skill = skill.lower()

        results = [
            candidate
            for candidate in results
            if any(
                skill == candidate_skill.lower()
                for candidate_skill in candidate["skills"]
            )
        ]

    if minimum_match_score is not None:

        results = [
            candidate
            for candidate in results
            if candidate["match_score"] >= minimum_match_score
        ]

    if minimum_interview_score is not None:

        results = [
            candidate
            for candidate in results
            if candidate["interview_score"] >= minimum_interview_score
        ]

    return results


# ============================================================
# Gemini HR Copilot
# ============================================================

def ask_hr_copilot(question, candidates):
    """
    Generate a natural-language HR Copilot response
    using the candidate data retrieved from the system.
    """

    candidate_data = json.dumps(
        candidates,
        indent=2
    )

    prompt = f"""
You are an AI HR Copilot.

You assist recruiters by analyzing candidate information
and providing concise, evidence-based recruitment insights.

IMPORTANT:
- Use ONLY the candidate information provided below.
- Do not invent candidate skills, experience, scores, or achievements.
- Do not make the final hiring decision.
- Present information as recruiter-supporting evidence.
- If there are no matching candidates, clearly say so.

RECRUITER QUESTION:
{question}

AVAILABLE CANDIDATE DATA:
{candidate_data}

Provide a useful answer to the recruiter's question.

Mention relevant:
- candidate names
- skills
- experience
- match scores
- interview scores

If appropriate, explain why candidates match the recruiter's
stated criteria.

Do not rank candidates unless the recruiter's question explicitly
asks for candidates ordered by a numerical criterion.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()


# ============================================================
# HR Copilot Query Processor
# ============================================================

def process_hr_query(
    question,
    skill=None,
    minimum_match_score=None,
    minimum_interview_score=None
):
    """
    Retrieve relevant candidates and generate
    an AI-powered HR Copilot response.
    """

    candidates = search_candidates(
        skill=skill,
        minimum_match_score=minimum_match_score,
        minimum_interview_score=minimum_interview_score
    )

    response = ask_hr_copilot(
        question=question,
        candidates=candidates
    )

    return {
        "question": question,
        "matching_candidates": candidates,
        "copilot_response": response
    }


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    print("\n========== HR COPILOT TEST ==========\n")

    question = """
    Show me candidates who have Python and TensorFlow experience
    and explain their interview performance.
    """

    result = process_hr_query(
        question=question,
        skill="TensorFlow",
        minimum_match_score=70
    )

    print("Recruiter Question:")
    print(result["question"])

    print("\nMatching Candidates:")

    for candidate in result["matching_candidates"]:

        print(
            f"- {candidate['name']} "
            f"| Match: {candidate['match_score']} "
            f"| Interview: {candidate['interview_score']}"
        )

    print("\n========== AI COPILOT RESPONSE ==========\n")

    print(result["copilot_response"])

    print("\nHR Copilot completed successfully.")