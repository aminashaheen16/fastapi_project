from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime


class FileAnalysisRequest(BaseModel):
    file_name: str
    content: str


class FileAnalysisResponse(BaseModel):
    id: str
    user_id: str
    file_name: str
    content: Optional[str] = None
    analysis: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[Union[List[str], str]] = None
    sentiment: Optional[str] = None
    language: Optional[str] = None
    created_at: Optional[str] = None


class AnalyzeTextRequest(BaseModel):
    text: str
    # user_id comes from JWT token, not the request body


class TranslateRequest(BaseModel):
    text: str
    target_lang: str


class ProofreadRequest(BaseModel):
    text: str
