from configs.config_loader import settings
from problem_generator import generate_problem
from problem_validator import validate_problem
from problem_reflection import reflect_problem
from reflection_validator import validate_reflection
from log import clear_log
import os

class CPPG:
    def __init__(self, skill_1, skill_2, story="") -> None:
        clear_log()
        self.skill_1 = skill_1
        self.skill_2 = skill_2
        self.story = story
        os.environ["GEMINI_API_KEY"] = settings.api_key

    def generate(self):
        problem = generate_problem(self.skill_1, self.skill_2, self.story)
        problem = validate_problem(problem, self.skill_1, self.skill_2)
        problem = reflect_problem(problem)
        # problem = validate_reflection()
        return problem

if __name__ == "__main__":
    cppg = CPPG("math", "graphs")
    print(cppg.generate())