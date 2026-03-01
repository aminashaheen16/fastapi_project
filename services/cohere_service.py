import cohere
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY is required")

co = cohere.ClientV2(api_key=COHERE_API_KEY)

def analyze_text(text: str) -> str:
    """تحليل النص باستخدام Cohere"""
    try:
        response = co.generate(
            model="command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": f"حلل النص التالي وأعطني فهمًا شاملاً: {text}"
                }
            ],
            max_tokens=1024
        )
        return response.message.content[0].text
    except Exception as e:
        return f"خطأ في التحليل: {str(e)}"

def summarize_text(text: str) -> str:
    """تلخيص النص"""
    try:
        response = co.generate(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"اختصر هذا النص في 3-4 جمل: {text}"
                }
            ],
            max_tokens=256
        )
        return response.message.content[0].text
    except Exception as e:
        return f"خطأ: {str(e)}"

def extract_keywords(text: str) -> list:
    """استخراج الكلمات المفتاحية"""
    try:
        response = co.generate(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"استخرج أهم 5-7 كلمات مفتاحية من هذا النص: {text}"
                }
            ],
            max_tokens=256
        )
        return response.message.content[0].text.split(",")
    except Exception as e:
        return [f"خطأ: {str(e)}"]


def detect_sentiment(text: str) -> str:
    """كشف شعور النص (إيجابي/سلبي/محايد)"""
    try:
        response = co.generate(
            model="command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": f"حدد شعور النص التالي بكلمة واحدة (positive، negative، neutral): {text}"
                }
            ],
            max_tokens=60
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"خطأ: {str(e)}"


def detect_language(text: str) -> str:
    """كشف لغة النص"""
    try:
        response = co.generate(
            model="command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": f"ما هي لغة النص التالي؟ {text}"
                }
            ],
            max_tokens=60
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"خطأ: {str(e)}"


def translate_text(text: str, target_lang: str) -> str:
    """ترجمة النص إلى اللغة الهدف"""
    try:
        response = co.generate(
            model="command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": f"ترجم النص التالي إلى {target_lang}: {text}"
                }
            ],
            max_tokens=512
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"خطأ: {str(e)}"


def proofread_text(text: str) -> str:
    """تدقيق النص وتحسينه"""
    try:
        response = co.generate(
            model="command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": f"قم بتدقيق النص التالي وإعادة كتابته بشكل أفضل مع الحفاظ على المعنى: {text}"
                }
            ],
            max_tokens=512
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"خطأ: {str(e)}"
