from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register
from src.configs.config_loader import settings
from src.workflow.generate_problem import GenProblemWorkflow
from src.workflow.solve_problem import GenSolutionWorkflow
from src.workflow.generate_testcase import GenTestWorkflow
import os

class CPPG:
    def __init__(self) -> None:
        os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY
        os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={settings.PHOENIX_API_KEY}"
        os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"
        tracer_provider = register(
            project_name="cppg",
            set_global_tracer_provider=False
        )
        LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

    async def generate_problem(self, min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story="") -> dict:
        result = await GenProblemWorkflow(min_difficulty, max_difficulty, skill_1, skill_2, story, timeout=300, verbose=True).run()
        return result

    async def solve_problem(self, problem: dict, language: str) -> str:
        result = await GenSolutionWorkflow(problem, language, timeout=120, verbose=True).run()
        return result

    async def generate_testcase(self, problem: dict) -> str:
        result = await GenTestWorkflow(problem, timeout=120, verbose=True).run()
        return result