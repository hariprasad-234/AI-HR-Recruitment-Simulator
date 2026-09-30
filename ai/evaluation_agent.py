import os
import json
from dotenv import load_dotenv
from google import genai

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


def evaluate_answer(question, candidate_answer):
    """
    Evaluate a candidate's interview answer.

    Evaluation criteria:
    - Technical Accuracy
    - Communication Clarity
    - Confidence
    - Overall Score
    - Feedback
    """

    prompt = f"""
You are an AI interview evaluation agent.

Evaluate the candidate's answer to the interview question below.

INTERVIEW QUESTION:
{question}

CANDIDATE ANSWER:
{candidate_answer}

Evaluate the answer using these criteria:

1. Technical Accuracy
   - Is the technical information correct?
   - Does the answer demonstrate understanding?

2. Communication Clarity
   - Is the answer clear and understandable?
   - Is it logically organized?

3. Confidence
   - Does the candidate communicate their answer confidently?
   - Avoid judging personality or making assumptions beyond the answer itself.

4. Overall Score
   - Give an overall score from 0 to 100 based on the quality and relevance
     of the answer.

5. Feedback
   - Give specific constructive feedback.
   - Mention what the candidate did well.
   - Mention what could be improved.

Return ONLY valid JSON in exactly this format:

{{
    "technical_accuracy": 0,
    "communication_clarity": 0,
    "confidence": 0,
    "overall_score": 0,
    "strengths": [
        "strength 1",
        "strength 2"
    ],
    "improvements": [
        "improvement 1",
        "improvement 2"
    ],
    "feedback": "Overall constructive feedback"
}}

All scores except overall_score must be between 0 and 10.
Overall_score must be between 0 and 100.
Do not include markdown or ``` around the JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    result_text = response.text.strip()

    # Remove markdown code fences if Gemini adds them
    if result_text.startswith("```"):
        result_text = result_text.replace("```json", "")
        result_text = result_text.replace("```", "")
        result_text = result_text.strip()

    try:
        evaluation = json.loads(result_text)
    except json.JSONDecodeError:
        print("Could not parse Gemini response as JSON.")
        print("Raw response:")
        print(result_text)
        return None

    return evaluation


if __name__ == "__main__":

    question = """
    Explain one machine learning project you have worked on.
    What was your technical approach and why did you choose it?
    """

    candidate_answer = """
    I worked on a solar panel defect detection project using machine
    learning. I used a VGG16 based model because it is a pretrained
    convolutional neural network that can extract image features.
    I used TensorFlow to train the model and OpenCV for image
    preprocessing. I also created a Streamlit dashboard so that
    users could upload an image and receive a prediction.
    """

    print("\n========== EVALUATION AGENT ==========\n")

    evaluation = evaluate_answer(
        question=question,
        candidate_answer=candidate_answer
    )

    if evaluation:

        print("Technical Accuracy:",
              evaluation["technical_accuracy"], "/ 10")

        print("Communication Clarity:",
              evaluation["communication_clarity"], "/ 10")

        print("Confidence:",
              evaluation["confidence"], "/ 10")

        print("Overall Score:",
              evaluation["overall_score"], "/ 100")

        print("\nStrengths:")

        for strength in evaluation["strengths"]:
            print("-", strength)

        print("\nImprovements:")

        for improvement in evaluation["improvements"]:
            print("-", improvement)

        print("\nFeedback:")
        print(evaluation["feedback"])

        print("\nEvaluation completed successfully.")