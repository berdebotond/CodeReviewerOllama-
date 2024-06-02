# Path: ./api.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from modules.code_reader.code_reader import CodeReader

app = FastAPI()

class CodeAnalysisRequest(BaseModel):
    github_url: str

@app.post("/analyze_code")
def analyze_code(request: CodeAnalysisRequest):
    try:
        code_reader = CodeReader(request.github_url)
        code_summary = code_reader.get_code_summery()
        return {"code_summary": code_summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
