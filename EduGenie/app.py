from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from google import genai

# Initialize the FastAPI app and tell it where the HTML files are

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize the NEW Google GenAI SDK (Paste your actual API key below)
API_KEY = "apikey"
client = genai.Client(api_key=API_KEY)

# Route 1: Load the homepage when the user visits the site
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"result": None})

# Route 2: Handle the form submission when the user clicks the button
@app.post("/generate")
async def generate_content(request: Request, topic: str = Form(...), action: str = Form(...)):
    if action == "learn":
        prompt = f"Explain the topic '{topic}' to a high school student. Format your response using basic HTML tags like <h3>, <p>, <ul>, <li>, and <strong>. Do NOT use markdown like ** or #."
    else:
        prompt = f"Generate a 3-question multiple choice quiz about '{topic}'. Include the answer key at the bottom. Format your response using basic HTML tags like <h3>, <p>, <ul>, <li>, and <strong>. Do NOT use markdown."

    try:
        # Use the newly updated client and active 3.5-flash model
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        ai_output = response.text
    except Exception as e:
        ai_output = f"<p>Error connecting to AI: {e}</p>"

    # Send the AI's answer back to the HTML page
    return templates.TemplateResponse(request=request, name="index.html", context={"topic": topic, "result": ai_output})

