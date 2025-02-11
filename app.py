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
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    request: Request,
    skill1: str = Form(...),
    skill2: str = Form(...),
    minDiff: int = Form(...),
    maxDiff: int = Form(...),
    story: str = Form("")
):
    cppg = CPPG()
    try:
        problem = await cppg.generate_problem(minDiff, maxDiff, skill1, skill2, story)
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
async def generate_solution(
    request: Request,
    problem: dict = Body(...),
    language: str = Body(...)
):
    cppg = CPPG()
    try:
        solution = await cppg.solve_problem(problem, language)
        return JSONResponse({"solution": solution})
    except Exception as e:
        logger.warning(str(e))
        return JSONResponse({"error": str(e)})

@app.post("/generate-test")
async def generate_test(
    request: Request,
    problem: dict = Body(...)
):
    cppg = CPPG()
    try:
        test_script = await cppg.generate_testcase(problem)
        return JSONResponse({"test_script": test_script})
    except Exception as e:
        logger.warning(str(e))
        return JSONResponse({"error": str(e)})