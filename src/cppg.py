from src.workflows.generate_problem import GenProblemWorkflow
from src.workflows.solve_problem import GenSolutionWorkflow
from src.workflows.generate_testcase import GenTestWorkflow
from src.configs.config_loader import settings

class CPPG:
    async def generate_problem(self, min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story="") -> dict:
        config = settings.GenProblemWorkflow
        result = await GenProblemWorkflow(min_difficulty, max_difficulty, skill_1, skill_2, story, timeout=config.timeout, verbose=config.verbose).run()
        return result

    async def solve_problem(self, problem: dict, language: str) -> str:
        config = settings.GenSolutionWorkflow
        result = await GenSolutionWorkflow(problem, language, timeout=config.timeout, verbose=config.verbose).run()
        return result

    async def generate_testcase(self, problem: dict) -> str:
        config = settings.GenTestWorkflow
        result = await GenTestWorkflow(problem, timeout=config.timeout, verbose=config.verbose).run()
        return result