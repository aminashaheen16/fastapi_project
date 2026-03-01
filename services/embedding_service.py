from services.supabase_config import get_supabase
from services.cohere_service import co
import uuid
import math


def create_embedding(user_id: str, text: str, title: str):
    """Create embedding and save to Supabase table"""
    try:
        supabase = get_supabase()

        # Generate vector
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

        return {"message": "Embedding created successfully ✅", "id": emb_id}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def search_embeddings(user_id: str, query: str, limit: int = 5):
    """Semantic search in user's embeddings"""
    try:
        supabase = get_supabase()

        # Generate search embedding
        response = co.embed(
            model="embed-english-v3.0",
            texts=[query],
            input_type="search_document"
        )
        query_vec = response.embeddings[0]

        # Fetch all user embeddings
        res = supabase.table("embeddings").select("*").eq("user_id", user_id).execute()
        data = res.data if res.data else []

        # Cosine similarity function
        def cosine(a, b):
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(y * y for y in b))
            return dot / (norm_a * norm_b + 1e-9)

        ranked = sorted(data, key=lambda item: cosine(query_vec, item.get("embedding", [])), reverse=True)
        top = ranked[:limit]
        return {"results": top}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def get_all_embeddings(user_id: str):
    """Return all embeddings for a user"""
    try:
        supabase = get_supabase()
        res = supabase.table("embeddings").select("*").eq("user_id", user_id).execute()
        return {"embeddings": res.data}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


def generate_embedding_only(text: str):
    """Generate embedding and return it without saving to database"""
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
        return {"error": f"Error: {str(e)}"}