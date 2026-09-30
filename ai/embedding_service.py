from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from resume_parser import (
    extract_text_from_pdf,
    clean_text,
    detect_sections,
    extract_resume_data
)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

model = SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# GENERATE EMBEDDING
# ============================================================

def generate_embedding(text):
    """
    Convert text into a numerical embedding.
    """

    embedding = model.encode(text)

    return embedding


# ============================================================
# CALCULATE COSINE SIMILARITY
# ============================================================

def calculate_similarity(text1, text2):
    """
    Calculate cosine similarity between two texts.
    """

    embedding1 = generate_embedding(text1)
    embedding2 = generate_embedding(text2)

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )[0][0]

    return float(similarity)


# ============================================================
# CONVERT STRUCTURED RESUME INTO TEXT
# ============================================================

def resume_to_text(resume_data):
    """
    Convert structured resume data into meaningful text
    for embedding generation.
    """

    parts = []

    # Personal information
    personal_info = resume_data.get(
        "personal_info",
        {}
    )

    if personal_info.get("name"):
        parts.append(
            personal_info["name"]
        )

    # Education
    for education in resume_data.get(
        "education",
        []
    ):

        for key in [
            "institution",
            "degree",
            "field",
            "duration",
            "cgpa"
        ]:

            value = education.get(key)

            if value:
                parts.append(str(value))

    # Skills
    skills = resume_data.get(
        "skills",
        []
    )

    if skills:

        parts.append(
            "Skills: " + ", ".join(skills)
        )

    # Experience
    experience = resume_data.get(
        "experience",
        []
    )

    if experience:

        parts.append(
            "Experience: " +
            " ".join(experience)
        )

    # Projects
    projects = resume_data.get(
        "projects",
        []
    )

    if projects:

        parts.append(
            "Projects: " +
            " ".join(projects)
        )

    # Certifications
    certifications = resume_data.get(
        "certifications",
        []
    )

    if certifications:

        parts.append(
            "Certifications: " +
            " ".join(certifications)
        )

    # Achievements
    achievements = resume_data.get(
        "achievements",
        []
    )

    if achievements:

        parts.append(
            "Achievements: " +
            " ".join(achievements)
        )

    return "\n".join(parts)


# ============================================================
# RESUME EMBEDDING
# ============================================================

def generate_resume_embedding(resume_data):
    """
    Generate an embedding from structured resume data.
    """

    resume_text = resume_to_text(
        resume_data
    )

    embedding = generate_embedding(
        resume_text
    )

    return embedding


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n========== RESUME EMBEDDING TEST ==========\n"
    )

    # --------------------------------------------------------
    # Ask for resume
    # --------------------------------------------------------

    pdf_path = input(
        "Enter the path to the resume PDF: "
    )

    # --------------------------------------------------------
    # Parse resume
    # --------------------------------------------------------

    raw_text = extract_text_from_pdf(
        pdf_path
    )

    cleaned_text = clean_text(
        raw_text
    )

    sections = detect_sections(
        cleaned_text
    )

    resume_data = extract_resume_data(
        sections
    )

    # --------------------------------------------------------
    # Convert resume to text
    # --------------------------------------------------------

    resume_text = resume_to_text(
        resume_data
    )

    print(
        "\n========== RESUME TEXT FOR EMBEDDING ==========\n"
    )

    print(resume_text)

    # --------------------------------------------------------
    # Generate embedding
    # --------------------------------------------------------

    embedding = generate_resume_embedding(
        resume_data
    )

    print(
        "\n========== EMBEDDING INFORMATION ==========\n"
    )

    print(
        "Embedding dimensions:",
        len(embedding)
    )

    print(
        "First 10 values:",
        embedding[:10]
    )