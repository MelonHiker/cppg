from src.cppg import CPPG
from src.configs.config_loader import settings
from random import choice
import os

if __name__ == "__main__":
    skill_1 = choice(settings.tags)
    skill_2 = choice(settings.tag_relations[skill_1])
    print(f"You choose {skill_1} and {skill_2}")

    story = input("Give me a story about this problem:\n")
    cppg = CPPG(skill_1, skill_2, story)

    file_name = "generated_problem.json"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)
    cppg.generate(file_path)