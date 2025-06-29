from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust for production for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("GOOGLE_API_KEY environment variable not found. Please set it.")
    raise ValueError("GOOGLE_API_KEY is not set.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")


class Chat(BaseModel):
    msg: str
    # ingredients: list[str]


@app.post("/")
def chat(data: Chat):
    if True:
        response = model.generate_content(
contents = f"""You are a friendly and knowledgeable fitness assistant. 
Always give clear, accurate, and beginner-friendly answers in a warm and encouraging tone.

After answering the user's question, suggest one or two specific follow-up questions they can ask next to help them reach their fitness goals more effectively.

User: {data.msg}""",
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
            ),
        )
        
        print(json.dumps(response.to_dict(), indent=2))

        # Access the text from the response
        print(response.text.strip())
        return {"response": response.text.strip()}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Serve index.html at the root URL ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_file_path = os.path.join("static", "index.html")
    if not os.path.exists(html_file_path):
        raise HTTPException(
            status_code=404, detail="index.html not found in static directory."
        )
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
