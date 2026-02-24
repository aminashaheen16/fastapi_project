# FastAPI LLM Project 🚀

مشروع FastAPI متكامل يدمج تقنيات الذكاء الاصطناعي من Cohere مع قاعدة بيانات Supabase ونظام حماية JWT.

## المميزات الأساسية ✨

- **نظام المستخدمين**: تسجيل، دخول، وحماية المسارات باستخدام JWT tokens.
- **تحليل النصوص والملفات**:
    - دعم رفع ملفات PDF واستخراج النصوص منها.
    - تحليل شامل للنص (تلخيص، كلمات مفتاحية، مشاعر، لغة).
    - ترجمة النصوص لأي لغة.
    - تدقيق لغوي وإملائي (Proofreading).
- **الدردشة الذكية**:
    - نظام محادثة يحفظ السياق (Context-aware chat).
    - سجل محادثات لكل مستخدم.
- **البحث الدلالي (Semantic Search)**:
    - تحويل النصوص إلى Embeddings.
    - البحث باستخدام pgvector في Supabase.

## التقنيات المستخدمة 🛠️

- **Backend**: FastAPI (Python)
- **AI Models**: Cohere (Command R+, Embed Arabic/English)
- **Database**: Supabase (PostgreSQL + pgvector)
- **Auth**: JWT (jose)
- **File Processing**: PyPDF

## هيكلة المشروع 📂

```
fastapi_project/
├── controllers/    # مسارات الـ API
├── models/         # نماذج البيانات (Pydantic)
├── services/       # منطق العمل والخدمات الخارجية
├── main.py         # نقطة انطلاق التطبيق
└── requirements.txt # المكتبات المطلوبة
```

## التشغيل 🚀

1. تثبيت المكتبات:
   ```bash
   pip install -r requirements.txt
   ```

2. إعداد ملف `.env`:
   ```env
   COHERE_API_KEY=your_key
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   SECRET_KEY=your_secret
   ```

3. تشغيل الخادم:
   ```bash
   uvicorn main:app --reload
   ```

## أهم المسارات (EndPoints) 📍

### Authentication
- `POST /api/auth/register`: تسجيل جديد
- `POST /api/auth/login`: تسجيل دخول (يعيد token)

### Chat
- `POST /api/chat`: التحدث مع الـ AI (يحفظ سياق المحادثة)
- `GET /api/chat/history`: سجل المحادثات
- `DELETE /api/chat/history`: مسح السجل

### Files & Analysis
- `POST /api/files/upload-pdf`: رفع وتحليل ملف PDF
- `POST /api/files/analyze`: تحليل نص مباشر
- `POST /api/files/translate`: ترجمة نص
- `POST /api/files/proofread`: تدقيق نص
- `GET /api/files/history`: تاريخ التحليلات
- `DELETE /api/files/history`: مسح تاريخ التحليلات

### Embeddings
- `POST /api/embedding/`: إنشاء embedding لنص
- `GET /api/embedding/search`: بحث دلالي في المحتوى المخزن

