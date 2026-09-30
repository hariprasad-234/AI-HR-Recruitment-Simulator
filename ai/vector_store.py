import chromadb
from pathlib import Path


# ============================================================
# CHROMA DATABASE
# ============================================================

DB_PATH = Path(__file__).parent / "chroma_db"

client = chromadb.PersistentClient(
    path=str(DB_PATH)
)


# ============================================================
# RESUME COLLECTION
# ============================================================

collection = client.get_or_create_collection(
    name="resume_documents"
)


# ============================================================
# TEXT CHUNKING
# ============================================================

def chunk_text(
    text,
    chunk_size=700,
    overlap=100
):
    words = text.split()

    if not words:
        return []

    chunks = []

    start = 0

    while start < len(words):

        end = min(
            start + chunk_size,
            len(words)
        )

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks


# ============================================================
# STORE RESUME
# ============================================================

def store_resume(
    candidate_id,
    resume_text
):

    chunks = chunk_text(
        resume_text
    )

    if not chunks:
        raise ValueError(
            "Resume contains no text."
        )

    ids = []

    metadatas = []

    for index in range(len(chunks)):

        ids.append(
            f"{candidate_id}_{index}"
        )

        metadatas.append({
            "candidate_id": candidate_id,
            "chunk_index": index
        })

    collection.upsert(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    return len(chunks)


# ============================================================
# SEARCH RESUME
# ============================================================

def search_resume(
    candidate_id,
    query,
    top_k=5
):

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={
            "candidate_id": candidate_id
        }
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    output = []

    for document, metadata in zip(
        documents,
        metadatas
    ):

        output.append({
            "text": document,
            "metadata": metadata
        })

    return output


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample_resume = """
    Python developer with experience in
    Machine Learning, TensorFlow, PyTorch,
    SQL, Flask and Computer Vision.

    Developed AI projects using VGG16,
    Streamlit and TensorFlow.
    """

    candidate_id = "candidate_001"

    count = store_resume(
        candidate_id,
        sample_resume
    )

    print(
        "Stored chunks:",
        count
    )

    results = search_resume(
        candidate_id,
        "What Python and machine learning experience does the candidate have?"
    )

    print(
        "\n========== RETRIEVED RESUME =========="
    )

    for result in results:

        print(
            "\n",
            result["text"]
        )