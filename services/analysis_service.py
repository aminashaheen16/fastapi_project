from services.supabase_config import get_supabase
from services.cohere_service import (
    analyze_text, summarize_text, extract_keywords, 
    detect_sentiment, detect_language, translate_text, proofread_text
)
from datetime import datetime
import uuid
import io
from pypdf import PdfReader


def analyze_file(user_id: str, file_name: str, content: str):
    """تحليل الملف وحفظ النتائج"""
    try:
        supabase = get_supabase()

        # تحليل النص
        analysis = analyze_text(content)
        summary = summarize_text(content)
        keywords = extract_keywords(content)
        sentiment = detect_sentiment(content)
        language = detect_language(content)

        # حفظ في Supabase
        analysis_id = str(uuid.uuid4())

        supabase.table("file_analysis").insert({
            "id": analysis_id,
            "user_id": user_id,
            "file_name": file_name,
            "content": content,
            "analysis": analysis,
            "summary": summary,
            "keywords": ",".join(keywords),
            "sentiment": sentiment,
            "language": language,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        return {
            "message": "تم التحليل بنجاح ✅",
            "analysis_id": analysis_id,
            "analysis": analysis,
            "summary": summary,
            "keywords": keywords,
            "sentiment": sentiment,
            "language": language
        }
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def get_analysis_history(user_id: str):
    """احصل على سجل التحليلات"""
    try:
        supabase = get_supabase()
        response = supabase.table("file_analysis").select("*").eq("user_id", user_id).execute()
        return {"analyses": response.data}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def get_analysis_by_id(analysis_id: str):
    """احصل على تفاصيل التحليل"""
    try:
        supabase = get_supabase()
        response = supabase.table("file_analysis").select("*").eq("id", analysis_id).execute()
        if not response.data:
            return {"error": "التحليل غير موجود"}
        return response.data[0]
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def clear_analysis_history(user_id: str):
    """حذف سجل التحليلات بالكامل"""
    try:
        supabase = get_supabase()
        supabase.table("file_analysis").delete().eq("user_id", user_id).execute()
        return {"message": "تم حذف سجل التحليلات بنجاح ✅"}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def analyze_pdf(user_id: str, file_name: str, file_bytes: bytes):
    """استخراج النص من PDF وتحليله"""
    try:
        # قراءة الـ PDF
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text_content = ""
        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"
        
        if not text_content.strip():
            return {"error": "لم يتم العثور على نص في ملف الـ PDF ❌"}

        # استدعاء التحليل العادي بعد استخراج النص
        return analyze_file(user_id, file_name, text_content)
    except Exception as e:
        return {"error": f"خطأ في قراءة ملف الـ PDF: {str(e)}"}


def translate_content(text: str, target_lang: str):
    """ترجمة النص"""
    result = translate_text(text, target_lang)
    return {"original": text, "translated": result, "target_lang": target_lang}


def proofread_content(text: str):
    """تدقيق النص"""
    result = proofread_text(text)
    return {"original": text, "proofread": result}
