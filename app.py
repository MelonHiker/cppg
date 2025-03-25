from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.log import setup_logger
from src.cppg import CPPG
from src.tools.code_executor import CodeExecutor
from contextlib import asynccontextmanager
from src.configs.config_loader import settings
import llama_index.core
import phoenix as px
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY

    dir_path = settings.phoenix.working_dir
    if (not os.path.exists(dir_path)):
        os.makedirs(dir_path)
    os.environ["PHOENIX_WORKING_DIR"] = dir_path

    llama_index.core.set_global_handler("arize_phoenix")

    px.launch_app(use_temp_dir=False)
    yield
    px.close_app()

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
logger = setup_logger()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/generate")
async def generate_get(request: Request):
    return templates.TemplateResponse("result.html", {"request": request, "problem": {}})

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

@app.post("/generate-tutorial")
async def generate_tutorial(
    request: Request,
    problem: dict = Body(...),
):
    cppg = CPPG()
    try:
        reflection = await cppg.generate_reflection(problem)
        return JSONResponse(reflection)
    except Exception as e:
        logger.warning(str(e))
        return JSONResponse({"error": str(e)})

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

@app.post("/run-solution")
async def run_code(request: Request, payload: dict = Body(...)):
    executor = CodeExecutor()
    code = payload.get("code", "")
    language = payload.get("language", "")
    stdin_input = payload.get("stdin_input", "")

    try:
        result = executor.run_code(code, language, stdin_input)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"execution_output": "", "error_message": str(e)})

@app.post("/run-test")
async def run_test(request: Request, payload: dict = Body(...)):
    executor = CodeExecutor()
    code = payload.get("code", "")
    language = payload.get("language", "python")
    stdin_input = payload.get("stdin_input", "")
    try:
        result = executor.run_code(code, language, stdin_input)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"execution_output": "", "error_message": str(e)})