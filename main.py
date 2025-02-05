from src.cppg import CPPG
import yaml

if __name__ == "__main__":
    skill_1 = "dp"
    skill_2 = "binary search"
    min_difficulty = 1600
    max_difficulty = 2000
    story = "MelonWaler ate a cat."

    cppg = CPPG()
    
    # generate problem
    problem = cppg.generate(min_difficulty, max_difficulty, skill_1, skill_2, story)

    # save problem
    file_path = "generated_problem.yaml"
    with open(file_path, "w") as f:
        yaml.safe_dump(problem, f)
    
    # with open(file_path, "r") as f:
    #     problem = yaml.safe_load(f)

    # solve problem
    code = cppg.solve(problem, "python")

    # save code
    file_name = "answer.py"
    with open("answer.py", "w") as f:
        f.write(code)