from pydantic import BaseModel
from typing import Optional


class FileAnalysisRequest(BaseModel):
    file_name: str
    content: str


class FileAnalysisResponse(BaseModel):
    id: str
    user_id: str
    file_name: str
    analysis: str
    summary: str
    keywords: list
    created_at: str


class AnalyzeTextRequest(BaseModel):
    text: str
    # user_id comes from JWT token, not the request body


class TranslateRequest(BaseModel):
    text: str
    target_lang: str


class ProofreadRequest(BaseModel):
    text: str
