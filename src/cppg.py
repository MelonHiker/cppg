from src.configs.config_loader import settings
from src.stage.problem_generator import generate_problem
from src.stage.problem_validator import validate_problem
from src.stage.problem_reflection import reflect_problem
from src.stage.reflection_validator import validate_reflection
from src.stage.problem_selector import select_problem
from src.stage.problem_solver import solve_problem
from src.stage.code_debugger import debug
from src.stage.code_tester import test_code
from src.stage.testcase_generator import testcase_generator
from src.log import clear_log, setup_logger
from tqdm import tqdm
from typing import List
import asyncio
import yaml
import os

class CPPG:
    def __init__(self) -> None:
        clear_log()
        os.environ["GEMINI_API_KEY"] = settings.api_key
        self.logger = setup_logger()
        self.number_of_sample = 5
        self.number_of_try = 20

    def generate(self, min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story="") -> dict:
        with tqdm(total=100) as pbar:
            pbar.set_description("Generating problem")
            problem = asyncio.run(self._generate_problem(min_difficulty, max_difficulty, skill_1, skill_2, story))
            pbar.update(40)
            
            pbar.set_description("Validating problem")
            problem = self._validate_problem(min_difficulty, max_difficulty, problem, skill_1, skill_2)
            pbar.update(20)
            
            pbar.set_description("Reflecting on problem")
            reflection = self._reflect_on_problem(problem)
            pbar.update(20)
            
            pbar.set_description("Validating reflection")
            result = self._validate_reflection(problem, reflection, skill_1, skill_2)
            pbar.update(20)
            
        return result

    def solve(self, problem: dict, language: str) -> str:
        code = self.load_code(solve_problem(problem, language, self.logger), language)
        response = test_code(code, problem["examples"])
        if (response == "Accept"):
            return code

        for _ in range(self.number_of_try):
            code = self.load_code(debug(problem, code, response, language, self.logger), language)
            response = test_code(code, problem["examples"])
            if (response == "Accept"):
                return code
        return "Exceeded the number of debugging attempts."

    def testcase(self, problem) -> str:
        return self.load_code(testcase_generator(problem, self.logger), "python")

    async def _generate_problem(self, min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story: str) -> str:
        tasks = [generate_problem(min_difficulty, max_difficulty, skill_1, skill_2, self.logger) for _ in range(self.number_of_sample)]
        responses = await asyncio.gather(*tasks)

        problems = []
        keys = ["statement", "explains"]
        for response in responses:
            problem = self.load_yaml(response, keys)
            problems.append(problem["statement"])

        return select_problem(problems, min_difficulty, max_difficulty, skill_1, skill_2, story, self.logger)

    def _validate_problem(self, min_difficulty: int, max_difficulty: int, problem: str, skill_1: str, skill_2: str) -> str:
        response = validate_problem(min_difficulty, max_difficulty, problem, skill_1, skill_2, self.logger)
        keys = ["problem", "explains"]
        return self.load_yaml(response, keys)["problem"]

    def _reflect_on_problem(self, problem: dict) -> str:
        return reflect_problem(problem, self.logger)

    def _validate_reflection(self, problem: dict, reflection: dict, skill_1: str, skill_2: str) -> dict:
        response = validate_reflection(problem, reflection, skill_1, skill_2, self.logger)
        keys = [
            "title", 
            "time_limit", 
            "memory_limit", 
            "description", 
            "input_constraints", 
            "output_constraints", 
            "examples", 
            "note", 
            "solution_in_natural_language", 
            "time_complexity", 
            "space_complexity", 
            "difficulty",
            "explanation"
        ]
        return self.load_yaml(response, keys)

    def load_code(self, response_text: str, language: str):
        response_text = response_text.rstrip("` \n")
        response_text = response_text.removeprefix(f'```{language}').rstrip('`')
        return response_text

    def load_yaml(self, response_text: str, keys_fix_yaml: List[str] = []) -> dict:
        response_text = response_text.rstrip("` \n")
        response_text = response_text.removeprefix('```yaml').rstrip('`')
        try:
            data = yaml.safe_load(response_text)
        except Exception as e:
            data = self._try_fix_yaml(response_text, keys_fix_yaml=keys_fix_yaml)
            if not data:
                self.logger.info(f"Failed to parse AI YAML prediction: {e}")
        return data

    def _try_fix_yaml(self, response_text: str, keys_fix_yaml: List[str] = []) -> dict:
        response_text_lines = response_text.split('\n')

        keys = keys_fix_yaml
        response_text_lines_copy = response_text_lines.copy()
        for i in range(0, len(response_text_lines_copy)):
            for key in keys:
                if response_text_lines_copy[i].strip().startswith(key) and not '|' in response_text_lines_copy[i]:
                    response_text_lines_copy[i] = response_text_lines_copy[i].replace(f'{key}',
                                                                                    f'{key} |-\n        ')
        try:
            data = yaml.safe_load('\n'.join(response_text_lines_copy))
            self.logger.info(f"Successfully parsed AI prediction after adding |-\n")
            return data
        except:
            raise "yaml parsing error"
