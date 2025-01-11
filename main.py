from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from src.cppg import CPPG

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class Example(BaseModel):
    input: str = Field(description="The sample input of the problem")
    output: str = Field(description="The sample output of the problem")

class Problem(BaseModel):
    title: str
    time_limit: str
    memory_limit: str
    description: str
    input_constraints: str
    output_constraints: str
    examples: list[Example]
    note: str
    solution_in_natural_language: str
    time_complexity: str
    space_complexity: str
    difficulty: str

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
def generate(
    request: Request,
    skill1: str = Form(...),
    skill2: str = Form(...),
    minDiff: int = Form(...),
    maxDiff: int = Form(...),
    story: str = Form("")
):
    cppg = CPPG()
    try:
        result_dict = cppg.generate(minDiff, maxDiff, skill1, skill2, story)
        result = Problem(**result_dict)
        return templates.TemplateResponse("result.html", {"request": request, "result": result})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)