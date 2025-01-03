from src.configs.config_loader import settings
from src.stage.problem_generator import generate_problem
from src.stage.problem_validator import validate_problem
from src.stage.problem_reflection import reflect_problem
from src.stage.reflection_validator import validate_reflection
from src.stage.check_problem_skills_and_difficulty import check_skills_difficulty
from src.log import clear_log
from tqdm import tqdm
import os

class CPPG:
    def __init__(self) -> None:
        clear_log()
        os.environ["GEMINI_API_KEY"] = settings.api_key

    def generate(self, min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story="") -> dict:
        with tqdm(total=100) as pbar:
            pbar.set_description("Generating problem")
            problem = self._generate_and_check_problem(min_difficulty, max_difficulty, skill_1, skill_2, story, pbar)
            pbar.update(20)
            
            pbar.set_description("Validating problem")
            problem = self._validate_problem(problem, skill_1, skill_2)
            pbar.update(20)
            
            pbar.set_description("Reflecting on problem")
            reflection = self._reflect_on_problem(problem)
            pbar.update(20)
            
            pbar.set_description("Validating reflection")
            result = self._validate_reflection(problem, reflection, skill_1, skill_2)
            pbar.n = 100
            
        return result

    def _generate_and_check_problem(self, min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story: str, pbar) -> str:
        while True:
            problem = generate_problem(min_difficulty, max_difficulty, skill_1, skill_2, story)
            pbar.update(5)
            if check_skills_difficulty(min_difficulty, max_difficulty, skill_1, skill_2, problem):
                break
        return problem

    def _validate_problem(self, problem: dict, skill_1: str, skill_2: str) -> str:
        return validate_problem(problem, skill_1, skill_2)

    def _reflect_on_problem(self, problem: dict) -> str:
        return reflect_problem(problem)

    def _validate_reflection(self, problem: dict, reflection: dict, skill_1: str, skill_2: str) -> dict:
        return validate_reflection(problem, reflection, skill_1, skill_2)