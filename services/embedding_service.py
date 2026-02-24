from services.supabase_config import get_supabase
from services.cohere_service import co
from datetime import datetime
import uuid


def create_embedding(user_id: str, text: str, title: str = ""):
    """إنشاء embedding للنص"""
    try:
        supabase = get_supabase()

        # استخدام Cohere للـ embedding
        embedding_response = co.embed(
            model="embed-english-v3.0",
            texts=[text],
            input_type="search_document"
        )

        embedding_vector = embedding_response.embeddings[0]
        embedding_id = str(uuid.uuid4())

        # حفظ في Supabase
        supabase.table("embeddings").insert({
            "id": embedding_id,
            "user_id": user_id,
            "title": title or "Untitled",
            "text": text,
            "embedding": embedding_vector,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        return {
            "embedding_id": embedding_id,
            "message": "تم إنشاء الـ embedding بنجاح ✅",
            "dimension": len(embedding_vector)
        }
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def search_embeddings(user_id: str, query: str, limit: int = 5):
    """البحث في الـ embeddings باستخدام pgvector"""
    try:
        supabase = get_supabase()

        # إنشاء embedding للـ query
        query_embedding_response = co.embed(
            model="embed-english-v3.0",
            texts=[query],
            input_type="search_query"
        )
        query_vector = query_embedding_response.embeddings[0]

        # البحث في Supabase باستخدام pgvector RPC
        response = supabase.rpc(
            "match_embeddings",
            {
                "query_embedding": query_vector,
                "match_user_id": user_id,
                "match_count": limit
            }
        ).execute()

        return {
            "query": query,
            "results": response.data
        }
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def get_all_embeddings(user_id: str):
    """احصل على جميع الـ embeddings"""
    try:
        supabase = get_supabase()
        response = supabase.table("embeddings").select("id, user_id, title, text, created_at").eq("user_id", user_id).execute()
        return {"embeddings": response.data}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}
