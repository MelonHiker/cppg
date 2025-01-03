from src.cppg import CPPG
from src.configs.config_loader import settings
from random import choice
import json
import os


if __name__ == "__main__":
    skill_1 = choice(settings.tags)
    skill_2 = choice(settings.tag_relations[skill_1])
    print(f"You choose {skill_1} and {skill_2}")

    min_difficulty = 1600
    max_difficulty = 2000

    story = input("Give me a story about this problem:\n")

    file_name = "generated_problem.json"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    cppg = CPPG()
    res = cppg.generate(min_difficulty, max_difficulty, skill_1, skill_2, story)
    with open(file_name, 'w') as f:
        json.dump(res, f)