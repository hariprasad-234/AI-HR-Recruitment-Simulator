from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_tfidf_similarity(resume_text, job_description):
    """
    Calculate TF-IDF cosine similarity between
    a resume and a job description.
    """

    documents = [
        resume_text,
        job_description
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return float(similarity)


def calculate_tfidf_percentage(resume_text, job_description):
    """
    Convert TF-IDF similarity into a percentage.
    """

    similarity = calculate_tfidf_similarity(
        resume_text,
        job_description
    )

    return round(similarity * 100, 2)


# ============================================================
# Test
# ============================================================

if __name__ == "__main__":

    resume = """
    Python developer with experience in Machine Learning,
    TensorFlow, PyTorch, SQL and Computer Vision.
    """

    job = """
    We are looking for a Python Machine Learning Developer
    with experience in Python, TensorFlow, PyTorch,
    SQL and Computer Vision.
    """

    score = calculate_tfidf_percentage(
        resume,
        job
    )

    print("\n========== TF-IDF TEST ==========\n")

    print("Resume:")
    print(resume)

    print("\nJob Description:")
    print(job)

    print("\nTF-IDF Similarity:", score, "%")

    print("\nTF-IDF test completed successfully.")