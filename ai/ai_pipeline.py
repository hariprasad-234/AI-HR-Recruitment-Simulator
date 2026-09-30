"""
AI HR Recruitment Simulator
============================

Complete AI Pipeline

Resume PDF
    ↓
Resume Text Extraction
    ↓
Resume Parsing
    ↓
TF-IDF + Embeddings + Skill Matching
    ↓
Hybrid Job Matching
    ↓
ChromaDB + RAG
    ↓
AI Interview Questions
    ↓
Candidate Answer
    ↓
AI Evaluation
    ↓
Final Candidate Report
"""

import os
import json


# ============================================================
# IMPORT EXISTING AI SERVICES
# ============================================================

from job_matching import (
    extract_text_from_pdf,
    analyze_resume_for_job
)

from vector_store import (
    store_resume
)

from interview_agent import (
    prepare_interview
)

# IMPORTANT:
# evaluation_agent.py contains evaluate_answer(),
# not evaluate_interview().
from evaluation_agent import (
    evaluate_answer
)


# ============================================================
# SAMPLE JOB DESCRIPTION
# ============================================================

JOB_DESCRIPTION = """
We are looking for a Python Machine Learning Developer.

Requirements:

Python programming
SQL
Machine Learning
Deep Learning
TensorFlow
PyTorch
Scikit-learn
Pandas
NumPy
Computer Vision
OpenCV
Flask
REST API development
Data Structures and Algorithms

The candidate should have experience developing
machine learning applications and APIs.

Experience with Flask and Computer Vision is preferred.
"""


# ============================================================
# RESUME PROCESSING
# ============================================================

def process_resume(pdf_path, candidate_id):
    """
    Extract resume text and store it in the vector database.
    """

    print("\n" + "=" * 70)
    print("STEP 1 - RESUME PROCESSING")
    print("=" * 70)

    print("\nReading resume PDF...")

    resume_text = extract_text_from_pdf(pdf_path)

    if not resume_text:
        raise ValueError(
            "No text could be extracted from the resume."
        )

    print("Resume extracted successfully.")

    print("\nResume characters:", len(resume_text))

    # Store resume in ChromaDB
    print("\nStoring resume in ChromaDB...")

    store_resume(
        candidate_id=candidate_id,
        resume_text=resume_text
    )

    print("Resume stored successfully.")

    return resume_text


# ============================================================
# JOB MATCHING
# ============================================================

def perform_job_matching(resume_text):
    """
    Perform hybrid job matching.

    Existing job_matching.py handles:

        - Semantic similarity
        - TF-IDF similarity
        - Skill matching
        - Hybrid score
    """

    print("\n" + "=" * 70)
    print("STEP 2 - HYBRID JOB MATCHING")
    print("=" * 70)

    print("\nAnalyzing resume against job description...")

    result = analyze_resume_for_job(
        resume_text,
        JOB_DESCRIPTION
    )

    print("\nJOB MATCH RESULT")
    print("-" * 50)

    # Semantic similarity
    if "semantic_similarity" in result:

        print(
            f"Semantic similarity : "
            f"{result['semantic_similarity']:.2f}%"
        )

    elif "similarity" in result:

        print(
            f"Semantic similarity : "
            f"{result['similarity'] * 100:.2f}%"
        )

    # TF-IDF similarity
    if "tfidf_similarity" in result:

        print(
            f"TF-IDF similarity   : "
            f"{result['tfidf_similarity']:.2f}%"
        )

    # Skill matching
    if "skill_match_score" in result:

        print(
            f"Skill match         : "
            f"{result['skill_match_score']:.2f}%"
        )

    # Hybrid score
    if "match_percentage" in result:

        print(
            f"Hybrid match score  : "
            f"{result['match_percentage']:.2f}%"
        )

    # Matched skills
    if "matched_skills" in result:

        print(
            f"Matched skills      : "
            f"{len(result['matched_skills'])}"
        )

    # Missing skills
    if "missing_skills" in result:

        print(
            f"Missing skills      : "
            f"{len(result['missing_skills'])}"
        )

    return result


# ============================================================
# AI INTERVIEW
# ============================================================

def generate_interview(candidate_id):
    """
    Generate candidate-specific interview questions
    using the existing RAG + Interview Agent.
    """

    print("\n" + "=" * 70)
    print("STEP 3 - AI INTERVIEW GENERATION")
    print("=" * 70)

    print("\nGenerating personalized interview questions...")

    interview = prepare_interview(
        candidate_id=candidate_id,
        job_description=JOB_DESCRIPTION
    )

    questions = interview["questions"]

    print("\nGenerated Questions:")
    print("-" * 50)

    for index, question in enumerate(
        questions,
        start=1
    ):

        print(
            f"\n{index}. {question}"
        )

    return interview


# ============================================================
# CANDIDATE ANSWER
# ============================================================

def get_candidate_answer(question):
    """
    Collect a text answer for demonstration.

    Later this can be replaced by Voice AI.
    """

    print("\n" + "-" * 70)
    print("CANDIDATE ANSWER")
    print("-" * 70)

    print("\nQuestion:")
    print(question)

    answer = input(
        "\nEnter candidate answer:\n> "
    ).strip()

    # Use sample answer if the user presses Enter
    if not answer:

        answer = (
            "I worked on a machine learning project "
            "using Python and VGG16 for image "
            "classification. I prepared the dataset, "
            "trained the model, evaluated its performance "
            "and deployed the application using Streamlit."
        )

        print(
            "\nUsing sample candidate answer for testing."
        )

    return answer


# ============================================================
# AI EVALUATION
# ============================================================

def evaluate_candidate_answer(
    question,
    answer
):
    """
    Evaluate candidate answer using Evaluation Agent.
    """

    print("\n" + "=" * 70)
    print("STEP 4 - AI ANSWER EVALUATION")
    print("=" * 70)

    print("\nEvaluating candidate response...")

    # IMPORTANT:
    # The actual function in evaluation_agent.py is
    # evaluate_answer(question, candidate_answer)
    evaluation = evaluate_answer(
        question=question,
        candidate_answer=answer
    )

    print("\nEVALUATION RESULT")
    print("-" * 50)

    if isinstance(
        evaluation,
        dict
    ):

        if "technical_accuracy" in evaluation:

            print(
                "Technical accuracy :",
                evaluation["technical_accuracy"]
            )

        if "communication_clarity" in evaluation:

            print(
                "Communication      :",
                evaluation["communication_clarity"]
            )

        if "confidence" in evaluation:

            print(
                "Confidence         :",
                evaluation["confidence"]
            )

        if "overall_score" in evaluation:

            print(
                "Overall score      :",
                evaluation["overall_score"]
            )

        if "feedback" in evaluation:

            print("\nFeedback:")

            print(
                evaluation["feedback"]
            )

        if "strengths" in evaluation:

            print("\nStrengths:")

            for strength in evaluation["strengths"]:

                print(
                    "-",
                    strength
                )

        if "improvements" in evaluation:

            print("\nImprovements:")

            for improvement in evaluation["improvements"]:

                print(
                    "-",
                    improvement
                )

    else:

        print(evaluation)

    return evaluation


# ============================================================
# FINAL REPORT
# ============================================================

def generate_final_report(
    candidate_id,
    match_result,
    interview,
    evaluation
):
    """
    Combine all AI outputs into one candidate report.
    """

    print("\n" + "=" * 70)
    print("FINAL AI CANDIDATE REPORT")
    print("=" * 70)

    report = {

        "candidate_id": candidate_id,

        "job": (
            "Python Machine Learning Developer"
        ),

        "job_matching": match_result,

        "interview": {

            "number_of_questions": len(
                interview.get(
                    "questions",
                    []
                )
            )
        },

        "evaluation": evaluation
    }

    print(
        json.dumps(
            report,
            indent=4,
            default=str
        )
    )

    return report


# ============================================================
# COMPLETE PIPELINE
# ============================================================

def run_pipeline(
    pdf_path,
    candidate_id="candidate_001"
):
    """
    Execute the complete AI recruitment pipeline.
    """

    print("\n")

    print("=" * 70)

    print(
        "       AI HR RECRUITMENT SIMULATOR"
    )

    print(
        "             COMPLETE AI PIPELINE"
    )

    print("=" * 70)


    # ========================================================
    # STEP 1
    # ========================================================

    resume_text = process_resume(
        pdf_path,
        candidate_id
    )


    # ========================================================
    # STEP 2
    # ========================================================

    match_result = perform_job_matching(
        resume_text
    )


    # ========================================================
    # STEP 3
    # ========================================================

    interview = generate_interview(
        candidate_id
    )

    questions = interview.get(
        "questions",
        []
    )

    if not questions:

        raise ValueError(
            "Interview Agent did not generate questions."
        )


    # ========================================================
    # STEP 4
    # ========================================================

    first_question = questions[0]

    answer = get_candidate_answer(
        first_question
    )


    # ========================================================
    # STEP 5
    # ========================================================

    evaluation = evaluate_candidate_answer(
        first_question,
        answer
    )


    # ========================================================
    # FINAL REPORT
    # ========================================================

    report = generate_final_report(
        candidate_id,
        match_result,
        interview,
        evaluation
    )

    print("\n" + "=" * 70)

    print(
        "COMPLETE AI PIPELINE FINISHED SUCCESSFULLY"
    )

    print("=" * 70)

    return report


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Ask for resume PDF
    # --------------------------------------------------------

    resume_path = input(
        "\nEnter the path to the candidate resume PDF: "
    ).strip()


    # --------------------------------------------------------
    # Check whether file exists
    # --------------------------------------------------------

    if not os.path.exists(
        resume_path
    ):

        print(
            "\nERROR: Resume file not found:"
            f"\n{resume_path}"
        )

        exit()


    # --------------------------------------------------------
    # Run complete pipeline
    # --------------------------------------------------------

    try:

        run_pipeline(
            pdf_path=resume_path,
            candidate_id="candidate_001"
        )

    except Exception as error:

        print(
            "\n" + "=" * 70
        )

        print(
            "PIPELINE ERROR"
        )

        print(
            "=" * 70
        )

        print(
            "\n",
            error
        )