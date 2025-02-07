from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.log import setup_logger
from src.cppg import CPPG

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
logger = setup_logger()

@app.get("/")
def index(request: Request):
    # Render the index page with a form for input.
    # Note: The form on index.html uses POST /generate.
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
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
        problem = cppg.generate(minDiff, maxDiff, skill1, skill2, story)
        # Render result page with problem dict.
        return templates.TemplateResponse("result.html", {
            "request": request,
            "problem": problem
        })
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })

@app.post("/generate-solution")
def generate_solution(
    request: Request,
    problem: dict = Body(...),
    language: str = Body(...)
):
    cppg = CPPG()
    try:
        solution = cppg.solve(problem, language)
        return JSONResponse({"solution": solution})
    except Exception as e:
        logger.warning(str(e))
        return JSONResponse({"error": str(e)})

@app.post("/generate-test")
def generate_test(
    request: Request,
    problem: dict = Body(...)
):
    cppg = CPPG()
    try:
        test_script = cppg.testcase(problem)
        return JSONResponse({"test_script": test_script})
    except Exception as e:
        logger.warning(str(e))
        return JSONResponse({"error": str(e)})