import re
import json
from google import genai
from google.genai import types


def get_client() -> genai.Client:
    return genai.Client(api_key='Gemini API Key')


MODEL = "gemini-2.5-flash"


def evaluate_answer(
    question_text: str,
    answer_text: str,
    expected_key_points: list,
    category: str = "General",
    difficulty: str = "medium",
) -> dict:
    client = get_client()

    key_points_text = "\n".join(
        f"{i + 1}. {p}" for i, p in enumerate(expected_key_points)
    )

    prompt = f"""You are an expert technical interviewer evaluating a candidate's answer. Analyze the response carefully and provide structured feedback.

INTERVIEW QUESTION:
{question_text}

CATEGORY: {category}
DIFFICULTY: {difficulty}

EXPECTED KEY POINTS (what a strong answer should cover):
{key_points_text}

CANDIDATE'S ANSWER:
"{answer_text}"

Evaluate the answer on these dimensions (score 0-10 each):
1. RELEVANCE: How relevant and on-topic is the answer?
2. CLARITY: How clear, organized, and articulate is the explanation?
3. TECHNICAL ACCURACY: How technically correct is the answer?
4. COMPLETENESS: How many key points are covered?
5. OVERALL: Overall quality of the answer

Also identify:
- Which expected key points were COVERED in the answer
- Which expected key points were MISSED
- Specific STRENGTHS of the answer
- Specific areas for IMPROVEMENT
- Overall SENTIMENT: positive, neutral, or negative

Return ONLY valid JSON in this exact format:
{{
  "scores": {{
    "relevance": 0,
    "clarity": 0,
    "technicalAccuracy": 0,
    "completeness": 0,
    "overall": 0
  }},
  "feedback": "2-3 sentence overall feedback",
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["improvement 1", "improvement 2"],
  "coveredKeyPoints": ["point covered"],
  "missedKeyPoints": ["point missed"],
  "sentiment": "positive"
}}"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert technical interviewer. You evaluate candidate answers fairly and constructively. Always return valid JSON.",
                max_output_tokens=8192,
            ),
        )
        content = response.text or "{}"
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return {
        "scores": {
            "relevance": 5,
            "clarity": 5,
            "technicalAccuracy": 5,
            "completeness": 5,
            "overall": 5,
        },
        "feedback": "Unable to generate feedback at this time.",
        "strengths": [],
        "improvements": [],
        "coveredKeyPoints": [],
        "missedKeyPoints": [],
        "sentiment": "neutral",
    }


def generate_report(role_name: str, answers: list) -> dict:
    client = get_client()

    if not answers:
        return {
            "overallScore": 0,
            "grade": "F",
            "totalQuestions": 0,
            "categoryScores": [],
            "topStrengths": [],
            "keyImprovements": [],
            "overallFeedback": "No answers provided.",
            "recommendation": "Pass",
        }

    total_score = sum(a["evaluation"]["scores"]["overall"] for a in answers)
    overall_score = round(total_score / len(answers), 1)

    grade = "F"
    if overall_score >= 9:
        grade = "A+"
    elif overall_score >= 8:
        grade = "A"
    elif overall_score >= 7:
        grade = "B"
    elif overall_score >= 6:
        grade = "C"
    elif overall_score >= 5:
        grade = "D"

    qa_summary = "\n\n".join(
        f"Q{i + 1}: {a['question_text']}\n"
        f"Score: {a['evaluation']['scores']['overall']}/10\n"
        f"Strengths: {', '.join(a['evaluation'].get('strengths', []))}\n"
        f"Improvements: {', '.join(a['evaluation'].get('improvements', []))}"
        for i, a in enumerate(answers)
    )

    prompt = f"""You are an expert interviewer generating a performance report for a candidate who completed an interview for the {role_name} role.

OVERALL SCORE: {overall_score}/10 ({grade})
QUESTIONS ANSWERED: {len(answers)}

QUESTION-BY-QUESTION SUMMARY:
{qa_summary}

Generate a comprehensive report. Return ONLY valid JSON:
{{
  "topStrengths": ["strength 1", "strength 2", "strength 3"],
  "keyImprovements": ["improvement 1", "improvement 2", "improvement 3"],
  "overallFeedback": "3-4 sentence feedback summary",
  "recommendation": "Strong Hire"
}}

The recommendation must be one of: "Strong Hire", "Hire", "Consider", "Pass", "Strong Pass"."""

    report_data = {}
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert technical interviewer generating fair, constructive performance reports. Always return valid JSON.",
                max_output_tokens=8192,
            ),
        )
        content = response.text or "{}"
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            report_data = json.loads(match.group())
    except Exception:
        pass

    all_strengths = [s for a in answers for s in a["evaluation"].get("strengths", [])]
    all_improvements = [s for a in answers for s in a["evaluation"].get("improvements", [])]

    category_map: dict = {}
    for a in answers:
        cat = a.get("category", "General")
        if cat not in category_map:
            category_map[cat] = {"total": 0, "count": 0}
        category_map[cat]["total"] += a["evaluation"]["scores"]["overall"]
        category_map[cat]["count"] += 1

    category_scores = [
        {
            "category": cat,
            "score": round(v["total"] / v["count"], 1),
            "count": v["count"],
        }
        for cat, v in category_map.items()
    ]

    return {
        "overallScore": overall_score,
        "grade": grade,
        "totalQuestions": len(answers),
        "categoryScores": category_scores,
        "topStrengths": report_data.get("topStrengths", all_strengths[:3]),
        "keyImprovements": report_data.get("keyImprovements", all_improvements[:3]),
        "overallFeedback": report_data.get(
            "overallFeedback", "Performance evaluation complete."
        ),
        "recommendation": report_data.get("recommendation", "Consider"),
    }


def transcribe_audio(audio_bytes: bytes) -> str:
    client = get_client()

    try:
        import base64
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Part(
                    inline_data=types.Blob(mime_type="audio/wav", data=audio_b64)
                ),
                types.Part(text="Transcribe this audio recording exactly as spoken. Return only the transcribed text, nothing else."),
            ],
        )
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {e}") from e
