from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from src.cppg import CPPG
import yaml

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
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    skill1: str = Form(...),
    skill2: str = Form(...),
    minDiff: int = Form(...),
    maxDiff: int = Form(...),
    story: str = Form("")
):
    if not (800 <= minDiff <= 3500 and 800 <= maxDiff <= 3500):
        raise HTTPException(status_code=400, detail="Difficulty must be between 800 and 3500.")
    if minDiff > maxDiff:
        raise HTTPException(status_code=400, detail="Minimum difficulty must be ≤ maximum difficulty.")
    if not skill1 or not skill2:
        raise HTTPException(status_code=400, detail="Both skills must be chosen.")

    # Read problem from pre-generated result
    # with open(".idea/generated_problem.yaml", "r") as f:
    #     result_dict = yaml.safe_load(f)

    cppg = CPPG()
    result_dict = cppg.generate(minDiff, maxDiff, skill1, skill2, story)

    result = Problem(**result_dict)
    return templates.TemplateResponse("result.html", {"request": request, "result": result})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)