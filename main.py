from fastapi import FastAPI
from pydantic import BaseModel
from src.chat import send_message
import uvicorn

app = FastAPI()

class Message(BaseModel):
    message: str

class Response(BaseModel):
    response: str

@app.post('/send-message', response_model=Response)
async def send_request(message:Message):
    response = send_message(message.message)
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
