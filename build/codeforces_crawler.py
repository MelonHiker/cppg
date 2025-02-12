from bs4 import BeautifulSoup
from build.rag_builder import RAGBuilder
import requests
import glob
import json
import os
import re

def fetch_problem_details(contest_id: int, index: str, rating: int, tags: list) -> str:
    file_path = f"./codeforces/{contest_id}{index}.json"
    if (os.path.exists(file_path)):
        print(f"{file_path} already exists.")
        return
    
    with open("./codeforces/failure.json", "r") as file:
        failure = json.load(file)
        if (f"{contest_id}{index}\n" in failure["failure"]):
            print(f"Already attempted to fetch problem {contest_id}{index}.")   
            return

    url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    headers = {"user-agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch problem details from Codeforces. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    dic = dict()
    dic["title"] = soup.find("div", class_="title").get_text(strip=True).split(" ", 1)[1]
    dic["time_limit"] = soup.find("div", class_="time-limit").get_text(separator=": ", strip=True)
    dic["memory_limit"] = soup.find("div", class_="memory-limit").get_text(separator=": ", strip=True)
    dic["problem_statement"] = ''.join([i for i in soup.find('div', 'header').next_sibling.get_text()])
    dic["input_spec"] = soup.find("div", class_="input-specification").get_text(separator="\n", strip=True)
    dic["output_spec"] = soup.find("div", class_="output-specification").get_text(separator="\n", strip=True)
    dic["examples"] = soup.find("div", class_="sample-test").get_text(separator="\n", strip=True)
    dic["notes"] = soup.find("div", class_="note").get_text(separator="\n", strip=True) if soup.find("div", class_="note") else ""
    dic["rating"] = rating
    dic["tags"] = tags
    dic["id"] = f"{contest_id}{index}"

    for key, value in dic.items():
        if (isinstance(value, str)):
            dic[key] = re.sub(r"\$\$\$(.*?)\$\$\$", r"$\1$", value)

    with open(file_path, "w") as file:
        json.dump(dic, file, indent=4)

    print(f"Successfully fetched problem {contest_id}{index}.")

def update_problems():
    url = f"https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch problems from Codeforces API. Status code: {response.status_code}")

    response = response.json()
    if (response["status"] != "OK"):
        raise Exception(f'status: {response["status"]}\ncomment:{response["comment"]}')
    
    problems = response["result"]["problems"]
    for problem in problems:
        if (not problem.get("tags") or "interactive" in problem["tags"] or any("special" in tag for tag in problem["tags"])):
            continue
        try:
            if (problem.get("rating")):
                fetch_problem_details(problem["contestId"], problem["index"], problem["rating"], problem["tags"])
            else:
                print(f"Problem {problem["contestId"]}{problem["index"]} didn't has rating.")
        except Exception as e:
            print(f'Fail to fetch problem {problem["contestId"]}{problem["index"]}: {e}')
            with open("./codeforces/failure.json", "r") as file:
                failure = json.load(file)
            with open("./codeforces/failure.json", "w") as file:
                failure["failure"].append(f"{problem["contestId"]}{problem["index"]}\n")
                json.dump(failure, file, indent=4)

def update_index():
    json_files = [f for f in glob.glob("./codeforces/*.json") if not f.endswith("index.json") and not f.endswith("failure.json")]
    
    table = dict()
    for file_path in json_files:
        with open(file_path, "r") as file:
            problem = json.load(file)

        for tag in problem["tags"]:
            if (tag not in table):
                table[tag] = list()
            table[tag].append(f"{file_path}")

    with open("./codeforces/index.json", "w") as file:
        json.dump(table, file, indent=4)

if __name__ == "__main__":
    update_problems()
    update_index()
    rag = RAGBuilder()
    rag.update_index()