from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from src.cppg import CPPG
import markdown2

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

class Example(BaseModel):
    input: str = Field(description="The sample input of the problem")
    output: str = Field(description="The sample output of the problem")

class Problem(BaseModel):
    title: str = Field(description="The title of the problem")
    time_limit: str
    memory_limit: str
    description: str = Field(description="The description of the problem")
    input_constraints: str
    output_constraints: str
    examples: list[Example] = Field(description="A list of examples for the problem")
    note: str = Field(description="Explains why the example input produces the corresponding example output")
    solution_in_natural_language: str = Field(description="The solution in natural language to the problem")
    time_complexity: str = Field(description="The time complexity of the solution")
    space_complexity: str = Field(description="The space complexity of the solution")
    difficulty: str = Field(description="The Codeforces difficulty of the problem (800-3500)")

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
        raise HTTPException(status_code=400, detail="Minimum difficulty must be less than or equal to maximum difficulty.")
    if not skill1 or not skill2:
        raise HTTPException(status_code=400, detail="Both skills must be chosen.")

    # Generate the problem using CPPG
    cppg = CPPG()
    result_dict = cppg.generate(minDiff, maxDiff, skill1, skill2, story)

    result = Problem(**result_dict)
    formatted_result = format_as_html(result)
    return templates.TemplateResponse("result.html", {"request": request, "result": result, "formatted_result": formatted_result})

def format_as_html(result: Problem):
    examples_html = "".join(
        f"""
        <div class="example">
            <h4>Input</h4>
            <pre style="white-space: pre-wrap;">{example.input}</pre>
            <h4>Output</h4>
            <pre style="white-space: pre-wrap;">{example.output}</pre>
        </div>
        """ for example in result.examples
    )

    html = f"""
    <div class="problem-statement">
        <div class="limits">
            <p>Time Limit: {result.time_limit} | Memory Limit: {result.memory_limit}</p>
        </div>
        <div class="section">
            <h3>Description</h3>
            <p style="white-space: pre-wrap;">{markdown2.markdown(result.description).strip()}</p>
        </div>
        <div class="section">
            <h3>Input Constraints</h3>
            <p style="white-space: pre-wrap;">{markdown2.markdown(result.input_constraints).strip()}</p>
        </div>
        <div class="section">
            <h3>Output Constraints</h3>
            <p style="white-space: pre-wrap;">{markdown2.markdown(result.output_constraints).strip()}</p>
        </div>
        <div class="section">
            <h3>Examples</h3>
            {examples_html.strip()}
        </div>
        <div class="section">
            <h3>Notes</h3>
            <p style="white-space: pre-wrap;">{markdown2.markdown(result.note).strip()}</p>
        </div>
        <div class="section">
            <h3>Solution in Natural Language</h3>
            <p style="white-space: pre-wrap;">{markdown2.markdown(result.solution_in_natural_language).strip()}</p>
        </div>
        <div class="section">
            <h3>Time Complexity</h3>
            <p style="white-space: pre-wrap;">{markdown2.markdown(result.time_complexity).strip()}</p>
        </div>
        <div class="section">
            <h3>Space Complexity</h3>
            <p style="white-space: pre-wrap;">{markdown2.markdown(result.space_complexity).strip()}</p>
        </div>
        <div class="section">
            <h3>Difficulty</h3>
            <p style="white-space: pre-wrap;">{markdown2.markdown(result.difficulty).strip()}</p>
        </div>
    </div>
    """
    return html

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)