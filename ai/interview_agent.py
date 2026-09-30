import os
from dotenv import load_dotenv
from google import genai

from rag_service import build_interview_context


# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found. Please check your .env file."
    )

# Create Gemini client
client = genai.Client(api_key=api_key)


def generate_interview_questions(
    candidate_id,
    job_description,
    number_of_questions=5
):
    """
    Generate personalized interview questions using:
    Resume + RAG context + Job Description + Gemini
    """

    # Retrieve relevant resume information using RAG
    resume_context = build_interview_context(
        candidate_id=candidate_id,
        job_description=job_description
    )

    prompt = f"""
You are an AI recruitment interview agent.

Your task is to generate personalized interview questions
for a candidate based ONLY on the candidate's resume context
and the provided job description.

CANDIDATE RESUME CONTEXT:
{resume_context}

JOB DESCRIPTION:
{job_description}

Generate exactly {number_of_questions} interview questions.

Requirements:
1. Questions must be relevant to the job.
2. Questions should be grounded in the candidate's resume.
3. Include technical questions.
4. Include questions about projects or previous experience.
5. Include at least one question that tests technical decision-making.
6. Do not invent experience that is not present in the resume context.
7. Avoid generic questions such as "Tell me about yourself".
8. Make the questions suitable for a real technical interview.

Return ONLY the questions as a numbered list.
Do not provide explanations or answers.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    generated_text = response.text.strip()

    # Convert numbered list into Python list
    questions = []

    for line in generated_text.splitlines():
        line = line.strip()

        if not line:
            continue

        # Remove common numbering formats
        if line[0].isdigit():
            question = line.split(".", 1)[-1].strip()

            if question:
                questions.append(question)

    return questions


def prepare_interview(candidate_id, job_description):
    """
    Prepare a complete AI interview for a candidate.
    """

    resume_context = build_interview_context(
        candidate_id=candidate_id,
        job_description=job_description
    )

    questions = generate_interview_questions(
        candidate_id=candidate_id,
        job_description=job_description,
        number_of_questions=5
    )

    return {
        "candidate_id": candidate_id,
        "resume_context": resume_context,
        "questions": questions
    }


if __name__ == "__main__":

    candidate_id = "candidate_001"

    job_description = """
    We are looking for a Python Machine Learning Developer
    with experience in Python, SQL, TensorFlow, PyTorch,
    Machine Learning, Computer Vision and Flask.

    The candidate should be able to develop machine learning
    applications and explain technical decisions clearly.
    """

    print("\n========== AI INTERVIEW AGENT ==========\n")

    result = prepare_interview(
        candidate_id=candidate_id,
        job_description=job_description
    )

    print("Candidate:", result["candidate_id"])

    print("\n========== RAG CONTEXT ==========\n")
    print(result["resume_context"])

    print("\n========== AI GENERATED QUESTIONS ==========\n")

    for index, question in enumerate(result["questions"], start=1):
        print(f"{index}. {question}")

    print("\nInterview generation completed successfully.")