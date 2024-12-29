from src.configs.config_loader import settings
from src.stage.problem_generator import generate_problem
from src.stage.problem_validator import validate_problem
from src.stage.problem_reflection import reflect_problem
from src.stage.reflection_validator import validate_reflection
from src.log import clear_log
from tqdm import tqdm
import json
import os

class CPPG:
    def __init__(self, skill_1, skill_2, story="") -> None:
        clear_log()
        self.skill_1 = skill_1
        self.skill_2 = skill_2
        self.story = story
        os.environ["GEMINI_API_KEY"] = settings.api_key

    def generate(self, file_path) -> None:
        with tqdm(total=100) as pbar:
            pbar.set_description("Generating problem")
            problem = generate_problem(self.skill_1, self.skill_2, self.story)
            pbar.update(20)
            
            pbar.set_description("Validating problem")
            problem = validate_problem(problem, self.skill_1, self.skill_2)
            pbar.update(20)

            pbar.set_description("Reflecting on problem")
            reflection = reflect_problem(problem)
            pbar.update(20)

            pbar.set_description("Validating reflection")
            problem = validate_reflection(problem, reflection, self.skill_1, self.skill_2)
            pbar.update(20)

            pbar.set_description("Save file")
            with open(file_path, 'w') as f:
                json.dump(problem, f)
            pbar.update(20)
    