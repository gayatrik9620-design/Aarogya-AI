import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
import uuid

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field

from backend.database import get_connection, init_db
from backend.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from backend.agent import get_health_agent_reply


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Aarogya AI Backend",
    description="AI Powered Health Monitoring System",
    version="1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class RegisterInput(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class ChatInput(BaseModel):
    message: str = Field(min_length=1, max_length=3000)


class FeedbackInput(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str = Field(default="", max_length=1000)


@app.get("/")
def home():
    return {"message": "Welcome to Aarogya AI Backend!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/auth/register")
def register(data: RegisterInput):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO users(name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (
                    data.name.strip(),
                    data.email.lower(),
                    hash_password(data.password),
                ),
            )
            user_id = cursor.lastrowid
    except Exception as e:
        if "UNIQUE" in str(e).upper():
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            )
        raise HTTPException(
            status_code=500,
            detail="Registration failed",
        )
    finally:
        conn.close()

    return {
        "message": "Registration successful",
        "user_id": user_id,
    }


@app.post("/api/auth/login")
def login(data: LoginInput):
    conn = get_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (data.email.lower(),),
        ).fetchone()
    finally:
        conn.close()

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return {
        "access_token": create_access_token(user["id"]),
        "token_type": "bearer",
    }


@app.get("/api/auth/me")
def profile(user=Depends(get_current_user)):
    return user


@app.post("/api/chat")
async def chat(
    data: ChatInput,
    user=Depends(get_current_user),
):
    clean_message = data.message.strip()
    if not clean_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        answer = await asyncio.to_thread(get_health_agent_reply, clean_message)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Health agent error: {e}",
        )

    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO chats(user_id, message, response)
                VALUES (?, ?, ?)
                """,
                (user["id"], clean_message, answer),
            )
            chat_id = cursor.lastrowid
    finally:
        conn.close()

    return {
        "chat_id": chat_id,
        "message": clean_message,
        "response": answer,
    }


@app.get("/api/chat/history")
def chat_history(user=Depends(get_current_user)):
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT id, message, response, created_at
            FROM chats
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 50
            """,
            (user["id"],),
        ).fetchall()
    finally:
        conn.close()

    return {"history": [dict(row) for row in rows]}


@app.post("/api/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    allowed = {".csv", ".json", ".txt"}
    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format",
        )

    content = await file.read(5 * 1024 * 1024 + 1)

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds 5 MB",
        )

    filename = f"user_{user['id']}_{uuid.uuid4().hex}{extension}"
    saved_path = UPLOAD_DIR / filename
    saved_path.write_bytes(content)

    conn = get_connection()
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO uploads(user_id, filename, saved_path)
                VALUES (?, ?, ?)
                """,
                (
                    user["id"],
                    Path(file.filename or "upload").name,
                    str(saved_path),
                ),
            )
    finally:
        conn.close()

    return {"message": "File uploaded successfully", "filename": filename}


@app.post("/api/feedback")
def feedback(
    data: FeedbackInput,
    user=Depends(get_current_user),
):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO feedback(user_id, rating, comment)
                VALUES (?, ?, ?)
                """,
                (user["id"], data.rating, data.comment),
            )
            feedback_id = cursor.lastrowid
    finally:
        conn.close()

    return {
        "message": "Feedback submitted successfully",
        "feedback_id": feedback_id,
    }


@app.get("/api/analytics")
def analytics(user=Depends(get_current_user)):
    conn = get_connection()
    try:
        chats = conn.execute(
            "SELECT COUNT(*) FROM chats WHERE user_id = ?",
            (user["id"],),
        ).fetchone()[0]

        uploads = conn.execute(
            "SELECT COUNT(*) FROM uploads WHERE user_id = ?",
            (user["id"],),
        ).fetchone()[0]

        feedbacks = conn.execute(
            "SELECT COUNT(*) FROM feedback WHERE user_id = ?",
            (user["id"],),
        ).fetchone()[0]
    finally:
        conn.close()

    return {
        "total_chats": chats,
        "total_uploads": uploads,
        "total_feedback": feedbacks,
    }