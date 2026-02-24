from fastapi import APIRouter, Depends, File, UploadFile
from models.request_model import RegisterRequest, LoginRequest
from models.analysis_model import AnalyzeTextRequest, TranslateRequest, ProofreadRequest
from models.chat_model import ChatRequest, EmbeddingRequest
from services.user_service import register_user, login_user
from services.analysis_service import (
    analyze_file, get_analysis_history, get_analysis_by_id, 
    analyze_pdf, translate_content, proofread_content, clear_analysis_history
)
from services.chat_service import chat, get_chat_history, clear_chat_history
from services.embedding_service import create_embedding, search_embeddings, get_all_embeddings
from services.auth import get_current_user

router = APIRouter()

# ========== ROOT ENDPOINT ==========
@router.get("/", tags=["Health"])
def root():
    return {"message": "FastAPI LLM API with Cohere 💗"}

@router.get("/health", tags=["Health"])
def health():
    return {"status": "healthy ✅"}

# ========== AUTHENTICATION ==========
@router.post("/auth/register", tags=["Authentication"])
def register(request: RegisterRequest):
    return register_user(request.username, request.email, request.password)

@router.post("/auth/login", tags=["Authentication"])
def login(request: LoginRequest):
    return login_user(request.email, request.password)

@router.get("/auth/me", tags=["Authentication"])
def get_me(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id, "message": "User authenticated ✅"}

# ========== CHAT ==========
@router.post("/chat", tags=["Chat"])
def chat_endpoint(request: ChatRequest, user_id: str = Depends(get_current_user)):
    """طرح سؤال والحصول على إجابة"""
    return chat(user_id, request.message)

@router.get("/chat/history", tags=["Chat"])
def history(user_id: str = Depends(get_current_user)):
    """احصل على سجل الدردشة"""
    return get_chat_history(user_id)

@router.delete("/chat/history", tags=["Chat"])
def clear_history(user_id: str = Depends(get_current_user)):
    """احذف سجل الدردشة"""
    return clear_chat_history(user_id)

# ========== FILES ==========
@router.post("/files/analyze", tags=["Files"])
def analyze(request: AnalyzeTextRequest, user_id: str = Depends(get_current_user)):
    """تحليل الملف/النص"""
    return analyze_file(user_id, "text_analysis", request.text)

@router.post("/files/upload-pdf", tags=["Files"])
async def upload_pdf(file: UploadFile = File(...), user_id: str = Depends(get_current_user)):
    """رفع ملف PDF وتحليله"""
    if not file.filename.lower().endswith(".pdf"):
        return {"error": "يرجى رفع ملف بصيغة PDF فقط ❌"}
    
    file_bytes = await file.read()
    return analyze_pdf(user_id, file.filename, file_bytes)

@router.get("/files/history", tags=["Files"])
def get_history(user_id: str = Depends(get_current_user)):
    """احصل على سجل التحليلات"""
    return get_analysis_history(user_id)

@router.delete("/files/history", tags=["Files"])
def delete_history(user_id: str = Depends(get_current_user)):
    """احذف سجل التحليلات"""
    return clear_analysis_history(user_id)

@router.get("/files/{analysis_id}", tags=["Files"])
def get_analysis_details(analysis_id: str, user_id: str = Depends(get_current_user)):
    """احصل على تفاصيل تحليل معين"""
    return get_analysis_by_id(analysis_id)

@router.post("/files/translate", tags=["Files"])
def translate(request: TranslateRequest, user_id: str = Depends(get_current_user)):
    """ترجمة نص"""
    return translate_content(request.text, request.target_lang)

@router.post("/files/proofread", tags=["Files"])
def proofread(request: ProofreadRequest, user_id: str = Depends(get_current_user)):
    """تدقيق نص لغوياً"""
    return proofread_content(request.text)

# ========== EMBEDDINGS ==========
@router.post("/embedding/", tags=["Embedding"])
def create_embedding_endpoint(request: EmbeddingRequest, user_id: str = Depends(get_current_user)):
    """Create Embedding"""
    return create_embedding(user_id, request.text, request.title)

@router.get("/embedding/search", tags=["Embedding"])
def search_embedding(query: str, limit: int = 5, user_id: str = Depends(get_current_user)):
    """البحث في الـ embeddings"""
    return search_embeddings(user_id, query, limit)

@router.get("/embedding/all", tags=["Embedding"])
def get_embeddings(user_id: str = Depends(get_current_user)):
    """احصل على جميع الـ embeddings"""
    return get_all_embeddings(user_id)