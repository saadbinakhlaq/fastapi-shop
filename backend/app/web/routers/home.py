import base64
import uuid

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from openai import OpenAI

client = OpenAI()

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/home",
    tags=["home"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/",
    response_class=HTMLResponse
)
def read_root(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate_image(request: Request, prompt: str = Form(...)):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        tools=[{"type": "image_generation"}],
    )

    image_data = [
        output.result
        for output in response.output
        if output.type == "image_generation_call"
    ]

    image_url = None
    if image_data:
        image_base64 = image_data[0]
        filename = f"static/images/generated_{uuid.uuid4().hex[:8]}.png"
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image_base64))
        image_url = "/" + filename  # relative path for static serving

    return templates.TemplateResponse("index.html", {"request": request, "image_url": image_url})

