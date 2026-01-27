from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(title="Backend Orchestrator")

AGENT_SERVICE_URL = "http://127.0.0.1:9000/process"

class ChatRequest(BaseModel):
    query: str

@app.post("/invoke")
async def handle_chat(payload: ChatRequest):
    try:
        # Просто пересылаем запрос в сервис агента
        response = requests.post(
            AGENT_SERVICE_URL, 
            json={"query": payload.query},
            timeout=60  # Модели нужно время на "подумать"
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Service Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
