from services.supabase_config import get_supabase
from services.jwt_service import create_access_token
import hashlib


def register_user(username: str, email: str, password: str):
    try:
        supabase = get_supabase()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        response = supabase.table("users").insert({
            "username": username,
            "email": email,
            "password": hashed_password
        }).execute()

        return {"message": "تم التسجيل بنجاح ✅", "user": response.data}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}


def login_user(email: str, password: str):
    try:
        supabase = get_supabase()
        response = supabase.table("users").select("*").eq("email", email).execute()

        if not response.data:
            return {"error": "المستخدم غير موجود ❌"}

        user = response.data[0]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if user["password"] == hashed_password:
            token = create_access_token(data={"sub": str(user["id"])})
            return {
                "message": "تسجيل الدخول ناجح ✅",
                "access_token": token,
                "token_type": "bearer",
                "user_id": user["id"],
                "username": user["username"]
            }
        else:
            return {"error": "كلمة المرور خاطئة ❌"}
    except Exception as e:
        return {"error": f"خطأ: {str(e)}"}