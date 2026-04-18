from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROMPT_ID = os.getenv("PROMPT_ID")
PROMPT_VERSION = os.getenv("PROMPT_VERSION")


@app.post("/chat")
def chat(data: dict):
    user_message = data.get("message")
    history = data.get("history", [])

    body = {
        "prompt": {
            "id": PROMPT_ID,
            "version": PROMPT_VERSION
        },
        "input": history if history else user_message
    }

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json=body
    )

    if response.status_code != 200:
        return {"error": response.text}

    data = response.json()
    # print("Full API response:==", data)  # Debugging line
    # answer = (
    #     data.get("output_text")
    #     or (data.get("output", [{}])[2].get("content", [{}])[0].get("text"))
    # )

    return {"reply": data}