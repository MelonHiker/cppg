from random import shuffle
import json

def get_random_problems(count: int, min_difficulty: int, max_difficulty: int, skill: str, ex_skill: str) -> list:
    with open("./codeforces/index.json", "r") as file:
        index = json.load(file)
    
    json_files = index[skill]
    if len(json_files) < count:
        raise Exception(f"Not enough problems to choose from: {len(json_files)}")
    shuffle(json_files)

    valid_problems = []
    for file_path in json_files:
        with open(file_path, "r") as file:
            problem = json.load(file)

        if (ex_skill in problem["tags"] or not problem.get("rating") or problem.get("rating") < min_difficulty or problem.get("rating") > max_difficulty):
            continue
        valid_problems.append(problem)
        if (len(valid_problems) >= count):
            break

    if (len(valid_problems) < count):
        raise Exception(f"Fail to get {count} problems")
    
    return valid_problems

if __name__ == "__main__":
    print(get_random_problems(3, 1800, 2000, "dp", None))