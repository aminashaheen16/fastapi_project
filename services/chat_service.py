from services.supabase_config import get_supabase
from services.cohere_service import co
from datetime import datetime
import uuid


def save_chat_message(user_id: str, message: str, response: str):
    """حفظ رسالة الدردشة"""
    try:
        supabase = get_supabase()
        chat_id = str(uuid.uuid4())

        supabase.table("chat_history").insert({
            "id": chat_id,
            "user_id": user_id,
            "message": message,
            "response": response,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        return {
            "chat_id": chat_id,
            "message": message,
            "response": response
        }
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def chat(user_id: str, message: str):
    """دردشة مع Cohere"""
    try:
        response = co.chat(
            model="command-a-03-2025",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        ai_response = response.message.content[0].text

        # حفظ في Database
        return save_chat_message(user_id, message, ai_response)
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def get_chat_history(user_id: str):
    """احصل على سجل الدردشة"""
    try:
        supabase = get_supabase()
        response = supabase.table("chat_history").select("*").eq("user_id", user_id).order("created_at", desc=False).execute()
        return {"history": response.data}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def clear_chat_history(user_id: str):
    """احذف سجل الدردشة"""
    try:
        supabase = get_supabase()
        supabase.table("chat_history").delete().eq("user_id", user_id).execute()
        return {"message": "تم حذف السجل بنجاح ✅"}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}
