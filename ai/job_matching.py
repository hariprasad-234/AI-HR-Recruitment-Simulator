"""
AI Job Matching Service
-----------------------

Compares a candidate resume with a job description using:

1. Sentence Transformer embeddings
2. Cosine similarity
3. TF-IDF similarity
4. Explicit skill matching

These signals are combined into a hybrid job-match score.
"""


# ============================================================
# IMPORTS
# ============================================================

import os

import numpy as np

from pypdf import PdfReader

from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity

from tfidf_service import calculate_tfidf_similarity


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "all-MiniLM-L6-v2"

print("\nLoading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Embedding model loaded successfully.")


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a resume PDF.
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"Resume file not found: {pdf_path}"
        )

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Basic text cleaning before processing.
    """

    if not text:
        return ""

    text = text.replace("\n", " ")

    text = " ".join(text.split())

    return text


# ============================================================
# EMBEDDING GENERATION
# ============================================================

def generate_embedding(text):
    """
    Convert text into a Sentence Transformer embedding.

    Returns:
        numpy array with shape (1, 384)
    """

    if not text or not text.strip():
        raise ValueError(
            "Cannot generate embedding from empty text."
        )

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    # Sentence Transformer returns a 1D vector.
    # cosine_similarity expects a 2D array.

    embedding = np.asarray(
        embedding
    ).reshape(1, -1)

    return embedding


# ============================================================
# COSINE SIMILARITY
# ============================================================

def calculate_cosine_similarity(
    resume_embedding,
    job_embedding
):
    """
    Calculate cosine similarity between
    resume and job embeddings.
    """

    resume_embedding = np.asarray(
        resume_embedding
    ).reshape(1, -1)

    job_embedding = np.asarray(
        job_embedding
    ).reshape(1, -1)

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )

    return float(
        similarity[0][0]
    )


# ============================================================
# SEMANTIC RESUME + JOB MATCHING
# ============================================================

def match_resume_with_job(
    resume_text,
    job_description
):
    """
    Compare resume text against a job description
    using Sentence Transformer embeddings.

    Returns:
        semantic similarity between -1 and 1
    """

    resume_text = clean_text(
        resume_text
    )

    job_description = clean_text(
        job_description
    )

    if not resume_text:
        raise ValueError(
            "Resume text is empty."
        )

    if not job_description:
        raise ValueError(
            "Job description is empty."
        )

    print(
        "\nGenerating resume embedding..."
    )

    resume_embedding = generate_embedding(
        resume_text
    )

    print(
        "Resume embedding generated."
    )

    print(
        "Generating job embedding..."
    )

    job_embedding = generate_embedding(
        job_description
    )

    print(
        "Job embedding generated."
    )

    similarity = calculate_cosine_similarity(
        resume_embedding,
        job_embedding
    )

    return similarity


# ============================================================
# SKILL ANALYSIS
# ============================================================

def analyze_skills(
    resume_text,
    job_description
):
    """
    Perform an explainable skill comparison.

    Skills mentioned in the job description are checked
    against the candidate resume.
    """

    common_skills = [

        "python",
        "java",
        "c++",
        "c",
        "sql",

        "machine learning",
        "deep learning",

        "tensorflow",
        "pytorch",
        "scikit-learn",

        "pandas",
        "numpy",

        "opencv",
        "flask",
        "fastapi",
        "django",

        "react",
        "javascript",
        "html",
        "css",

        "git",
        "github",

        "docker",

        "aws",
        "azure",

        "nlp",
        "computer vision",

        "data structures",
        "algorithms",

        "rest api",

        "postgresql",
        "mongodb"
    ]

    resume_lower = resume_text.lower()

    job_lower = job_description.lower()

    required_skills = []

    matched_skills = []

    missing_skills = []

    for skill in common_skills:

        # Skill mentioned in job description

        if skill in job_lower:

            required_skills.append(
                skill
            )

            # Skill also present in resume

            if skill in resume_lower:

                matched_skills.append(
                    skill
                )

            else:

                missing_skills.append(
                    skill
                )

    return (
        required_skills,
        matched_skills,
        missing_skills
    )


# ============================================================
# COMPLETE HYBRID MATCH ANALYSIS
# ============================================================

def analyze_resume_for_job(
    resume_text,
    job_description
):
    """
    Complete hybrid job matching analysis.

    Combines:

    1. Semantic similarity
       Sentence Transformer embeddings

    2. TF-IDF similarity
       Lexical/text similarity

    3. Skill matching
       Explicit skill overlap

    Final score:

        50% Semantic Similarity
        30% Skill Match
        20% TF-IDF Similarity
    """

    # --------------------------------------------------------
    # Clean input text
    # --------------------------------------------------------

    resume_text = clean_text(
        resume_text
    )

    job_description = clean_text(
        job_description
    )

    if not resume_text:
        raise ValueError(
            "Resume text is empty."
        )

    if not job_description:
        raise ValueError(
            "Job description is empty."
        )

    # ========================================================
    # 1. SEMANTIC SIMILARITY
    # ========================================================

    print(
        "\nGenerating resume embedding..."
    )

    resume_embedding = generate_embedding(
        resume_text
    )

    print(
        "Resume embedding generated."
    )

    print(
        "Generating job embedding..."
    )

    job_embedding = generate_embedding(
        job_description
    )

    print(
        "Job embedding generated."
    )

    semantic_similarity = calculate_cosine_similarity(
        resume_embedding,
        job_embedding
    )

    # Convert to percentage

    semantic_percentage = max(
        0,
        min(
            100,
            semantic_similarity * 100
        )
    )

    # ========================================================
    # 2. TF-IDF SIMILARITY
    # ========================================================

    print(
        "Calculating TF-IDF similarity..."
    )

    tfidf_similarity = calculate_tfidf_similarity(
        resume_text,
        job_description
    )

    tfidf_percentage = max(
        0,
        min(
            100,
            tfidf_similarity * 100
        )
    )

    # ========================================================
    # 3. SKILL ANALYSIS
    # ========================================================

    (
        required_skills,
        matched_skills,
        missing_skills
    ) = analyze_skills(
        resume_text,
        job_description
    )

    # ========================================================
    # 4. SKILL MATCH PERCENTAGE
    # ========================================================

    if required_skills:

        skill_percentage = (
            len(matched_skills)
            /
            len(required_skills)
        ) * 100

    else:

        skill_percentage = 0

    # ========================================================
    # 5. HYBRID MATCH SCORE
    # ========================================================

    hybrid_score = (

        (semantic_percentage * 0.50)

        +

        (skill_percentage * 0.30)

        +

        (tfidf_percentage * 0.20)
    )

    hybrid_score = max(
        0,
        min(
            100,
            hybrid_score
        )
    )

    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        # Semantic similarity

        "similarity": semantic_similarity,

        "semantic_percentage":
            semantic_percentage,

        # TF-IDF

        "tfidf_similarity":
            tfidf_similarity,

        "tfidf_percentage":
            tfidf_percentage,

        # Skills

        "skill_percentage":
            skill_percentage,

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        # Final score

        "match_percentage":
            hybrid_score
    }


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print("\n")

    print("=" * 60)

    print(
        "          AI HYBRID JOB MATCHING TEST"
    )

    print("=" * 60)

    # --------------------------------------------------------
    # Resume input
    # --------------------------------------------------------

    pdf_path = input(
        "\nEnter the path to the resume PDF: "
    ).strip()

    try:

        print(
            "\nExtracting resume text..."
        )

        resume_text = extract_text_from_pdf(
            pdf_path
        )

        if not resume_text:

            raise ValueError(
                "No text could be extracted from the PDF."
            )

        print(
            "Resume text extracted successfully."
        )

    except Exception as error:

        print(
            "\nERROR while reading resume:"
        )

        print(error)

        exit()


    # --------------------------------------------------------
    # Job description
    # --------------------------------------------------------

    job_description = """

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

    Experience with Flask and computer vision is preferred.

    """


    # --------------------------------------------------------
    # Perform analysis
    # --------------------------------------------------------

    try:

        result = analyze_resume_for_job(
            resume_text,
            job_description
        )

    except Exception as error:

        print(
            "\nERROR during job matching:"
        )

        print(error)

        exit()


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    print("\n")

    print("=" * 60)

    print(
        "                MATCH RESULT"
    )

    print("=" * 60)


    # --------------------------------------------------------
    # Semantic similarity
    # --------------------------------------------------------

    print(

        f"\nSemantic similarity : "
        f"{result['semantic_percentage']:.2f}%"
    )


    # --------------------------------------------------------
    # TF-IDF similarity
    # --------------------------------------------------------

    print(

        f"TF-IDF similarity   : "
        f"{result['tfidf_percentage']:.2f}%"
    )


    # --------------------------------------------------------
    # Skill match
    # --------------------------------------------------------

    print(

        f"Skill match         : "
        f"{result['skill_percentage']:.2f}%"
    )


    # --------------------------------------------------------
    # Hybrid score
    # --------------------------------------------------------

    print(

        f"Hybrid match score  : "
        f"{result['match_percentage']:.2f}%"
    )


    # --------------------------------------------------------
    # Required skills
    # --------------------------------------------------------

    print("\n")

    print(
        "--- REQUIRED SKILLS ---"
    )

    if result["required_skills"]:

        for skill in result[
            "required_skills"
        ]:

            print(
                f"• {skill}"
            )

    else:

        print(
            "No predefined skills detected."
        )


    # --------------------------------------------------------
    # Matched skills
    # --------------------------------------------------------

    print("\n")

    print(
        "--- MATCHED SKILLS ---"
    )

    if result["matched_skills"]:

        for skill in result[
            "matched_skills"
        ]:

            print(
                f"✓ {skill}"
            )

    else:

        print(
            "No direct skill matches detected."
        )


    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    print("\n")

    print(
        "--- MISSING / WEAK SKILLS ---"
    )

    if result["missing_skills"]:

        for skill in result[
            "missing_skills"
        ]:

            print(
                f"• {skill}"
            )

    else:

        print(
            "No missing skills detected."
        )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n")

    print("=" * 60)

    print(
        "                 FINAL SUMMARY"
    )

    print("=" * 60)


    print(

        f"\nSemantic similarity : "
        f"{result['semantic_percentage']:.2f}%"
    )


    print(

        f"TF-IDF similarity   : "
        f"{result['tfidf_percentage']:.2f}%"
    )


    print(

        f"Skill match         : "
        f"{result['skill_percentage']:.2f}%"
    )


    print(

        f"Hybrid match score  : "
        f"{result['match_percentage']:.2f}%"
    )


    print(

        f"Matched skills      : "
        f"{len(result['matched_skills'])}"
    )


    print(

        f"Missing skills      : "
        f"{len(result['missing_skills'])}"
    )


    print(
        "\nHybrid job matching completed successfully."
    )