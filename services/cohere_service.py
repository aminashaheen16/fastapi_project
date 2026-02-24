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
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"حلل النص التالي وأعطني فهمًا شاملاً: {text}"
                }
            ]
        )
        return response.message.content[0].text
    except Exception as e:
        return f"خطأ في التحليل: {str(e)}"


def summarize_text(text: str) -> str:
    """تلخيص النص"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"اختصر هذا النص في 3-4 جمل: {text}"
                }
            ]
        )
        return response.message.content[0].text
    except Exception as e:
        return f"خطأ: {str(e)}"



def extract_keywords(text: str) -> list:
    """استخراج الكلمات المفتاحية"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"استخرج أهم 5-7 كلمات مفتاحية من هذا النص وافصل بينهم بفاصلة فقط: {text}"
                }
            ]
        )
        return response.message.content[0].text.split(",")
    except Exception as e:
        return [f"خطأ: {str(e)}"]


def detect_sentiment(text: str) -> str:
    """تحليل المشاعر في النص (إيجابي، سلبي، محايد)"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"حدد مشاعر النص التالي (إيجابي، سلبي، محايد) بكلمة واحدة فقط: {text}"
                }
            ]
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"خطأ: {str(e)}"


def detect_language(text: str) -> str:
    """تحديد لغة النص"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"ما هي لغة هذا النص؟ أجب بكلمة واحدة فقط (مثلاً: Arabic, English): {text}"
                }
            ]
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"خطأ: {str(e)}"


def translate_text(text: str, target_lang: str) -> str:
    """ترجمة النص إلى اللغة المستهدفة"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"ترجم النص التالي إلى {target_lang}: {text}"
                }
            ]
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"خطأ في الترجمة: {str(e)}"


def proofread_text(text: str) -> str:
    """تدقيق وقواعد اللغة"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"قم بتدقيق النص التالي لغوياً وإملائياً وأعد كتابته بشكل أفضل: {text}"
                }
            ]
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"خطأ في التدقيق: {str(e)}"
