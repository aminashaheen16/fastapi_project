from services.supabase_config import get_supabase
from services.cohere_service import co
import uuid
import math


def create_embedding(user_id: str, text: str, title: str):
    """إنشاء embedding وحفظه في جدول Supabase"""
    try:
        supabase = get_supabase()

        # توليد المتجه
        embedding_response = co.embed(
            model="embed-english-v3.0",
            texts=[text],
            input_type="search_document"
        )
        embedding_vector = embedding_response.embeddings[0]

        emb_id = str(uuid.uuid4())
        supabase.table("embeddings").insert({
            "id": emb_id,
            "user_id": user_id,
            "text": text,
            "title": title,
            "embedding": embedding_vector
        }).execute()

        return {"message": "تم إنشاء embedding بنجاح ✅", "id": emb_id}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def search_embeddings(user_id: str, query: str, limit: int = 5):
    """البحث الدلالي في الـ embeddings للمستخدم"""
    try:
        supabase = get_supabase()

        # توليد embedding للبحث
        response = co.embed(
            model="embed-english-v3.0",
            texts=[query],
            input_type="search_document"
        )
        query_vec = response.embeddings[0]

        # جلب كل embeddings الخاصة بالمستخدم
        res = supabase.table("embeddings").select("*").eq("user_id", user_id).execute()
        data = res.data if res.data else []

        # دالة تشابه كوزاين
        def cosine(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(y * y for y in b))
            return dot / (norm_a * norm_b + 1e-9)

        ranked = sorted(data, key=lambda item: cosine(query_vec, item.get("embedding", [])), reverse=True)
        top = ranked[:limit]
        return {"results": top}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def get_all_embeddings(user_id: str):
    """إرجاع جميع embeddings لمستخدم"""
    try:
        supabase = get_supabase()
        res = supabase.table("embeddings").select("*").eq("user_id", user_id).execute()
        return {"embeddings": res.data}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def generate_embedding_only(text: str):
    """إنشاء embedding وإرجاعه فقط بدون حفظه في قاعدة البيانات"""
    try:
        embedding_response = co.embed(
            model="embed-english-v3.0",
            texts=[text],
            input_type="search_document"
        )

        embedding_vector = embedding_response.embeddings[0]

        return {
            "embedding": embedding_vector,
            "dimension": len(embedding_vector)
        }

    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}