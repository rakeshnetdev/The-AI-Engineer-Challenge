from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
import os
# from dotenv import load_dotenv

# load_dotenv()

app = FastAPI()

# CORS so the frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def _get_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=api_key,
    )

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def ui():
    """Serve the chat frontend at /ui."""
    root_dir = Path(__file__).resolve().parent.parent
    for path in (root_dir / "public" / "index.html", root_dir / "frontend" / "index.html"):
        if path.exists():
            return FileResponse(path)
    raise HTTPException(status_code=404, detail="Frontend not found")

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    client = _get_client()
    if not client:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured. Add it in Vercel Project Settings → Environment Variables.",
        )

    try:
        user_message = request.message
        response = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905:together",  # Or :fastest, :fireworks-ai, etc.
            messages=[
                {"role": "system", "content": "You are a supportive mental coach."},
                {"role": "user", "content": user_message}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling OpenAI API: {str(e)}")
