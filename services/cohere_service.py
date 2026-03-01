import cohere
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("COHERE_API_KEY is required")

co = cohere.ClientV2(api_key=COHERE_API_KEY)

def analyze_text(text: str) -> str:
    """Analyze text using Cohere"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze the following text and provide a comprehensive understanding: {text}"
                }
            ]
        )
        return response.message.content[0].text
    except Exception as e:
        return f"Analysis error: {str(e)}"

def summarize_text(text: str) -> str:
    """Summarize text"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this text in 3-4 sentences: {text}"
                }
            ]
        )
        return response.message.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def extract_keywords(text: str) -> list:
    """Extract keywords"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"Extract the top 5-7 keywords from this text: {text}"
                }
            ]
        )
        return response.message.content[0].text.split(",")
    except Exception as e:
        return [f"Error: {str(e)}"]


def detect_sentiment(text: str) -> str:
    """Detect sentiment of the text (positive/negative/neutral)"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"Identify the sentiment of the following text with one word (positive, negative, neutral): {text}"
                }
            ]
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def detect_language(text: str) -> str:
    """Detect language of the text"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"What is the language of the following text? {text}"
                }
            ]
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def translate_text(text: str, target_lang: str) -> str:
    """Translate text to target language"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following text to {target_lang}: {text}"
                }
            ]
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def proofread_text(text: str) -> str:
    """Proofread and improve text"""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"Proofread the following text and rewrite it better while maintaining the meaning: {text}"
                }
            ]
        )
        return response.message.content[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
