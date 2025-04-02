from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ Import CORS middleware
from pydantic import BaseModel
from analyzer import analyze_question

app = FastAPI()

# ✅ Allow frontend to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, change to your frontend URL like ["https://asknyai.in"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    platform: str
    user: str
    message: str

@app.post("/analyze")
async def analyze(query: Query):
    response = analyze_question(query.message)
    return {"reply": response}
