"""
Intent detection utility for recruitment assistant.
"""

from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
import structlog
import os

logger = structlog.get_logger(__name__)

INTENT_CLASSES = ["resume_review", "tech_interview", "hr_interview", "company_info"]

INTENT_DETECTION_PROMPT = f"""
You are an intent classifier for a candidate recruitment portal.
Classify the user's input into exactly one of these categories:
{', '.join(INTENT_CLASSES)}

- "resume_review": User asks to review a resume, evaluate skills for a role, or improve a resume.
- "tech_interview": User asks for technical questions, mock technical interview, or tech concept explanation.
- "hr_interview": User asks for behavioral questions, HR questions, STAR method, or soft skills mock.
- "company_info": User asks about the company's background, mission, vision, achievements, or interview process.

Return ONLY the category name as a plain string, nothing else.
If you are completely unsure, return "company_info" as fallback.
"""

def detect_intent(user_msg: str, api_key: Optional[str] = None) -> str:
    """Detect the intent of the user message."""
    api_key = api_key or os.getenv("GOOGLE_API_KEY") or "mock-key"
    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.0,
        )
        response = model.invoke([
            {"role": "system", "content": INTENT_DETECTION_PROMPT},
            {"role": "user", "content": user_msg},
        ])
        intent = response.content.strip().lower()
        if intent in INTENT_CLASSES:
            return intent
        return "company_info"
    except Exception as e:
        logger.error("Intent detection failed", error=str(e))
        return "company_info"
