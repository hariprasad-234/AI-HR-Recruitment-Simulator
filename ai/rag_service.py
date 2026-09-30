from vector_store import search_resume


# ============================================================
# RAG RETRIEVAL
# ============================================================

def retrieve_resume_context(
    candidate_id,
    query,
    top_k=3
):
    """
    Retrieve the most relevant parts of a candidate's
    resume for a given query.
    """

    results = search_resume(
        candidate_id=candidate_id,
        query=query,
        top_k=top_k
    )

    if not results:
        return ""

    context_parts = []

    for result in results:

        text = result.get("text", "").strip()

        if text:
            context_parts.append(text)

    return "\n\n".join(context_parts)


# ============================================================
# BUILD INTERVIEW CONTEXT
# ============================================================

def build_interview_context(
    candidate_id,
    job_description
):
    """
    Retrieve resume information relevant to the job.
    """

    query = f"""
    Candidate resume information relevant to this job:

    {job_description}

    Focus on:
    - technical skills
    - projects
    - education
    - work experience
    - certifications
    - relevant achievements
    """

    context = retrieve_resume_context(
        candidate_id=candidate_id,
        query=query,
        top_k=5
    )

    return context


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    candidate_id = "candidate_001"

    job_description = """
    We are looking for a Python Machine Learning Developer
    with experience in Python, SQL, TensorFlow, PyTorch,
    Machine Learning, Computer Vision and Flask.
    """

    print(
        "\n========== RAG TEST ==========\n"
    )

    context = build_interview_context(
        candidate_id=candidate_id,
        job_description=job_description
    )

    if context:

        print("Retrieved candidate context:\n")

        print(context)

    else:

        print(
            "No relevant resume information found."
        )
        