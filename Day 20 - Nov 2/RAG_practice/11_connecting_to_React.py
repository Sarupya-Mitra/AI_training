from rag_core import PROJECT_DIR, search_chunks
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
import time
from concurrent.futures import ThreadPoolExecutor

load_dotenv(".env")
if not os.getenv("KEY"):
    raise SystemExit("Add KEY to the existing .env file.")
api_key = os.getenv("KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODELS = [{
    "id" : "openrouter/free",
    "name" : "OpenRouter Free"
},
    {
        "id" : "nvidia/nemotron-3.5-lightning:free",
        "name": " Nvidia Nemotron 3.5 lightning "
    },
    {
        "id" : "nvidia/nemotron-3.5-super-vl:free",
        "name": " Nvidia Nemotron 3.5 super-vl "
    },
    {
        "id" : "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "name": " Nvidia Nemotron 3.5 nano omni "
    },
    {
        "id" : "liquid/lfm-2.5-2.6b:free",
        "name" : "LiquidAI LFM(2.5-2.6B)"
    },
    {
        "id" : "google/gemma-4-31b-it:free",
        "name" : "Google Gemma 4-31B"
    }
]

class Questions(BaseModel):
    question: str
    models : list[str] = Field(min_value=1,max_value=3)

@app.get("/models")
def get_models():
    return MODELS

def generate_answer(model, prompt):

    start_time = time.perf_counter()

    try:
        response = client.responses.create(
            model=model,
            instructions=(
                "You are a careful document Q&A assistant. "
                "Answer using only the supplied reference chunks."
            ),
            input=prompt
        )

        elapsed = time.perf_counter() - start_time

        return {
            "requested_model": model,
            "actual_model": response.model,
            "answer": response.output_text,
            "response_time": round(elapsed, 3),
            "accuracy": None,
            "tokens": (
                response.usage.total_tokens
                if response.usage else None
            ),
            "error": None
        }

    except Exception as error:
        return {
            "requested_model": model,
            "actual_model": None,
            "answer": None,
            "response_time": round(
                time.perf_counter() - start_time, 3
            ),
            "accuracy": None,
            "tokens": None,
            "error": str(error)
        }
@app.post("/ask")
def ask_question(request : Questions):
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Missing API key"
        )

    allowed_models = {m["id"] for m in MODELS}

    if len(set(request.models)) != len(request.models):
        raise HTTPException(
            status_code=400,
            detail="Duplicate models are not allowed"
        )

    if not set(request.models).issubset(allowed_models):
        raise HTTPException(
            status_code=400,
            detail="Invalid model selection"
        )

    # Retrieve context only once
    matches = search_chunks(request.question, top_k=3)

    context = "\n\n".join(
        f"[SOURCE {item['id']} — {item['source']}]\n"
        f"{item['text']}"
        for item in matches
    )

    prompt = f"""
        Answer using ONLY the reference chunks below.

        If the answer is unavailable, say:
        I could not find that information in the provided document.

        REFERENCE CHUNKS:
        {context}

        USER QUESTION:
        {request.question}
        """

    # Execute the selected models concurrently
    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = [
            executor.submit(generate_answer, model, prompt)
            for model in request.models
        ]

        results = [future.result() for future in futures]

    return {
        "question": request.question,
        "results": results
    }