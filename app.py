from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.log import setup_logger
from src.cppg import CPPG
from src.tools.code_executor import CodeExecutor

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
        # problem = await cppg.generate_problem(minDiff, maxDiff, skill1, skill2, story)

        # test
        problem = {"title": "Forest Cutting", "time_limit": "1 second", "memory_limit": "256 megabytes", "description": "In a lush forest, there are $N$ trees, each with a specific height and value. You are equipped with a tree-cutting machine and your goal is to maximize the total value of trees you harvest within a given time limit.\n\nTo operate the machine, you must first choose a cutting power, denoted by a positive integer $P$. Once you have selected $P$, the time it takes to cut down the $i$-th tree, which has height $H_i$, is given by the formula $\\lceil \\frac{H_i}{P} \\rceil = \\lfloor \\frac{H_i + P - 1}{P} \\rfloor = (H_i + P - 1) // P$, where $//$ represents integer division.\n\nYou have a total time limit $T$ to cut trees. You need to decide on a single cutting power $P$ and a subset of trees to cut. The total time spent cutting the chosen trees must not exceed $T$. Your objective is to maximize the sum of the values of the trees you cut.\n\nGiven the heights $H_i$ and values $V_i$ of $N$ trees, and a time limit $T$, find the maximum total value of trees you can harvest.", "input_constraints": "- $1 \\le N \\le 1000$\n- $1 \\le H_i \\le 10^5$\n- $1 \\le V_i \\le 10^5$\n- $1 \\le T \\le 10^6$", "output_constraints": "- Output a single integer, representing the maximum total value of harvested trees.", "examples": [{"input": "2 3\n5 10\n3 7", "output": "17"}, {"input": "3 5\n10 5\n5 8\n2 3", "output": "16"}], "note": "In the first example, if we choose a cutting power $P=3$.\n- For the first tree with height $H_1=5$, cutting time is $(5+3-1)//3 = 2$.\n- For the second tree with height $H_2=3$, cutting time is $(3+3-1)//3 = 1$.\nIf we cut both trees, the total time is $2+1=3$, which is within the time limit $T=3$. The total value is $10+7=17$. It can be verified that this is the maximum value achievable.\n\nIn the second example, if we choose a cutting power $P=5$.\n- For the first tree with height $H_1=10$, cutting time is $(10+5-1)//5 = 2$.\n- For the second tree with height $H_2=5$, cutting time is $(5+5-1)//5 = 1$.\n- For the third tree with height $H_3=2$, cutting time is $(2+5-1)//5 = 1$.\nIf we cut all three trees, the total time is $2+1+1=4$, which is within the time limit $T=5$. The total value is $5+8+3=16$. It can be verified that this is the maximum value achievable.", "solution_in_natural_language": "To solve this problem, we need to find the optimal cutting power $P$ and the best subset of trees to cut to maximize the total value within the given time limit $T$. We can iterate through possible values of the cutting power $P$. For each chosen $P$, we can calculate the time required to cut each tree using the formula $\\lceil H_i / P \\rceil = (H_i + P - 1) // P$. Once we have the cutting times for all trees for a given $P$, we face a 0/1 knapsack problem. We want to select a subset of trees such that the sum of their cutting times is no more than $T$, and the sum of their values is maximized. We can solve this 0/1 knapsack problem using dynamic programming.\n\nFor each possible cutting power $P$ (we can iterate $P$ from 1 up to a reasonable limit, like 2000, or up to the maximum height of any tree, or time limit $T$, whichever is smaller or a combination like $\\min(\\max(H_i), T, 2000)$), we perform the following steps:\n1. Calculate the cutting time $time_i = (H_i + P - 1) // P$ for each tree $i$.\n2. Use dynamic programming to solve the 0/1 knapsack problem. Let $dp[i][j]$ be the maximum value obtainable using the first $i$ trees and a total time limit of $j$. The transition is:\n   $dp[i][j] = dp[i-1][j]$ (if we don't cut the $i$-th tree)\n   If $j \\ge time_i$, then $dp[i][j] = \\max(dp[i][j], dp[i-1][j - time_i] + V_i)$ (if we cut the $i$-th tree).\n3. After calculating $dp[N][T]$ for the current $P$, this is the maximum value we can get with cutting power $P$.\n4. Keep track of the maximum value obtained across all tested values of $P$.\n\nThe final maximum value is the answer.  A reasonable range for $P$ to iterate over is from 1 to 2000, as beyond this, the cutting times tend to stabilize, and exploring further values of $P$ may not significantly improve the result, especially given the constraints.", "time_complexity": "Let $P_{max}$ be the maximum value of cutting power we iterate through. Let's assume $P_{max} \\approx 2000$. For each value of $P$, we solve a 0/1 knapsack problem using dynamic programming, which takes $O(N \\times T)$ time. Therefore, the total time complexity is $O(P_{max} \\times N \\times T)$. With $P_{max} \\approx 2000$, $N \\le 1000$, and $T \\le 10^6$, the complexity is approximately $O(2000 \\times 1000 \\times 10^6) = O(2 \\times 10^{12})$. While this might seem large, with efficient implementation, it might pass within the time limit of 1 second, especially if the actual number of operations is less in practice. If we consider $P_{max} = \\min(\\max(H_i), T)$, and in the worst case $\\max(H_i) \\approx 10^5$ and $T \\approx 10^6$, the complexity would be $O(\\min(\\max(H_i), T) \\times N \\times T)$.", "space_complexity": "The space complexity is dominated by the dynamic programming table used for the 0/1 knapsack problem, which is of size $O(N \\times T)$. We can reuse this table for each value of $P$. Thus, the space complexity is $O(N \\times T)$.", "tags": ["dynamic programming", "knapsack"], "explanation": "For the first example (input `2 3`, trees `[5, 10], [3, 7]`), if we choose cutting power $P=3$, the cutting times are $[\\lceil 5/3 \\rceil, \\lceil 3/3 \\rceil] = [2, 1]$. The total time is $2+1=3$, which is within the limit $T=3$. The total value is $10+7=17$. By trying other cutting powers and subsets, we can verify that 17 is the maximum achievable value.\n\nFor the second example (input `3 5`, trees `[10, 5], [5, 8], [2, 3]`), if we choose cutting power $P=5$, the cutting times are $[\\lceil 10/5 \\rceil, \\lceil 5/5 \\rceil, \\lceil 2/5 \\rceil] = [2, 1, 1]$. The total time is $2+1+1=4$, which is within the limit $T=5$. The total value is $5+8+3=16$. By trying other cutting powers and subsets, we can verify that 16 is the maximum achievable value.\n\nThe solution iterates through a range of cutting powers $P$. For each $P$, it calculates the cutting time for each tree. Then, it uses dynamic programming to solve the 0/1 knapsack problem to find the maximum value of trees that can be cut within the time limit $T$ using the chosen power $P$. Finally, it takes the maximum value among all considered cutting powers."}

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

# New run-test endpoint for test tab executions.
@app.post("/run-test")
async def run_test(request: Request, payload: dict = Body(...)):
    executor = CodeExecutor()
    code = payload.get("code", "")
    # Use "python" as default for test tab if not provided.
    language = payload.get("language", "python")
    stdin_input = payload.get("stdin_input", "")
    try:
        result = executor.run_code(code, language, stdin_input)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"execution_output": "", "error_message": str(e)})