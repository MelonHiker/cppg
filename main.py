from src.cppg import CPPG
import yaml

if __name__ == "__main__":
    skill_1 = "dp"
    skill_2 = "binary search"
    print(f"You choose {skill_1} and {skill_2}")

    min_difficulty = 1600
    max_difficulty = 2000

    story = "I ate a cat."

    cppg = CPPG()
    problem = cppg.generate(min_difficulty, max_difficulty, skill_1, skill_2, story)

    file_name = "generated_problem.yaml"
    with open(file_name, 'w') as f:
        yaml.dump(problem, f)
    
    code = cppg.solve(problem, "c++")

    file_name = "code.cpp"
    with open(file_name, 'w') as f:
        f.write(code)