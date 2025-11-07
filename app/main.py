from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .services.pipeline import correct_paragraph

app = FastAPI(title="Khmer Spell Checker")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "output": ""})

@app.post("/", response_class=HTMLResponse)
async def process_text(request: Request, input_text: str = Form(...)):
    corrected_text = correct_paragraph(input_text)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "input_text": input_text, "output": corrected_text}
    )
