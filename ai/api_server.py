from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from interview_agent import generate_interview_questions
from evaluation_agent import evaluate_answer


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="AI HR Recruitment Simulator API",
    description="Backend API for the AI-powered recruitment platform",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Models
# ============================================================

class InterviewRequest(BaseModel):
    candidate_id: str
    job_description: str
    number_of_questions: int = 5


class EvaluationRequest(BaseModel):
    question: str
    candidate_answer: str


# ============================================================
# Basic Endpoints
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI HR Recruitment Simulator API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI HR Recruitment Simulator"
    }


# ============================================================
# Interview Generation
# ============================================================

@app.post("/interview/generate")
def generate_interview(request: InterviewRequest):

    questions = generate_interview_questions(
        candidate_id=request.candidate_id,
        job_description=request.job_description,
        number_of_questions=request.number_of_questions
    )

    return {
        "candidate_id": request.candidate_id,
        "questions": questions
    }


# ============================================================
# Interview Evaluation
# ============================================================

@app.post("/interview/evaluate")
def evaluate_interview(request: EvaluationRequest):

    evaluation = evaluate_answer(
        question=request.question,
        candidate_answer=request.candidate_answer
    )

    return {
        "question": request.question,
        "candidate_answer": request.candidate_answer,
        "evaluation": evaluation
    }


# ============================================================
# Run Server
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )