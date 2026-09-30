from faster_whisper import WhisperModel

from evaluation_agent import evaluate_answer


# Load Whisper model
model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)


def speech_to_text(audio_file):
    """
    Convert an audio file into text using Whisper.
    """

    segments, info = model.transcribe(
        audio_file,
        beam_size=5
    )

    transcript = []

    for segment in segments:
        transcript.append(segment.text.strip())

    return " ".join(transcript)


def evaluate_voice_answer(question, audio_file):
    """
    Convert spoken answer to text and evaluate the transcript.
    """

    # Step 1: Speech → Text
    transcript = speech_to_text(audio_file)

    # Step 2: Text → Evaluation Agent
    evaluation = evaluate_answer(
        question=question,
        candidate_answer=transcript
    )

    return {
        "question": question,
        "transcript": transcript,
        "evaluation": evaluation
    }


if __name__ == "__main__":

    print("\n========== VOICE INTERVIEW TEST ==========\n")

    question = """
    Explain one machine learning project you have worked on.
    What was your technical approach and why did you choose it?
    """

    audio_file = "interviewer_answer.m4a"

    try:

        result = evaluate_voice_answer(
            question=question,
            audio_file=audio_file
        )

        print("Interview Question:")
        print(question)

        print("\n========== TRANSCRIPT ==========\n")
        print(result["transcript"])

        evaluation = result["evaluation"]

        print("\n========== AI EVALUATION ==========\n")

        print(
            "Technical Accuracy:",
            evaluation["technical_accuracy"],
            "/ 10"
        )

        print(
            "Communication Clarity:",
            evaluation["communication_clarity"],
            "/ 10"
        )

        print(
            "Confidence:",
            evaluation["confidence"],
            "/ 10"
        )

        print(
            "Overall Score:",
            evaluation["overall_score"],
            "/ 100"
        )

        print("\nStrengths:")

        for strength in evaluation["strengths"]:
            print("-", strength)

        print("\nImprovements:")

        for improvement in evaluation["improvements"]:
            print("-", improvement)

        print("\nFeedback:")
        print(evaluation["feedback"])

        print("\nVoice interview evaluation completed successfully.")

    except Exception as e:

        print("Error:", e)