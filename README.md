# FastAPI LLM Project 🚀

A comprehensive FastAPI project integrating AI technologies from Cohere with Supabase database and JWT security system.

## Key Features ✨

- **User System**: Registration, login, and path protection using JWT tokens.
- **Text & File Analysis**:
    - Support for uploading PDF files and extracting text from them.
    - Comprehensive text analysis (summarization, keywords, sentiment, language).
    - Text translation to any language.
    - Proofreading and grammar check.
- **Smart Chat**:
    - Context-aware chat system.
    - Conversation history for each user.
- **Semantic Search**:
    - Convert text to Embeddings.
    - Search using pgvector in Supabase.

## Technologies Used 🛠️

- **Backend**: FastAPI (Python)
- **AI Models**: Cohere (Command R+, Embed English/Arabic)
- **Database**: Supabase (PostgreSQL + pgvector)
- **Auth**: JWT (jose)
- **File Processing**: PyPDF

## Project Structure 📂

```
fastapi_project/
├── controllers/    # API routes
├── models/         # Data models (Pydantic)
├── services/       # Business logic and external services
├── main.py         # Application entry point
└── requirements.txt # Required libraries
```

## Running the Project 🚀

1. Install libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. Setup `.env` file:
   ```env
   COHERE_API_KEY=your_key
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   SECRET_KEY=your_secret
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Key Endpoints 📍

### Authentication
- `POST /api/auth/register`: New registration
- `POST /api/auth/login`: Login (returns token)

### Chat
- `POST /api/chat`: Talk to AI (saves conversation context)
- `GET /api/chat/history`: Conversation history
- `DELETE /api/chat/history`: Clear history

### Files & Analysis
- `POST /api/files/upload-pdf`: Upload and analyze PDF file
- `POST /api/files/analyze`: Direct text analysis
- `POST /api/files/translate`: Translate text
- `POST /api/files/proofread`: Proofread text
- `GET /api/files/history`: Analysis history
- `DELETE /api/files/history`: Clear analysis history

### Embeddings
- `POST /api/embedding/`: Create embedding for text
- `GET /api/embedding/search`: Semantic search in stored content
