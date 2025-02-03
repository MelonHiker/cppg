from bs4 import BeautifulSoup
import requests
import json
import os
from pprint import pprint

def fetch_tutorial(blog_url: str):
    url = f"https://codeforces.com{blog_url}"
    headers = {"user-agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")

    tutorial = soup.find("div", class_="ttypography")
    return str(tutorial)

def fetch_problem_details(contest_id: int, index: str, rating: int) -> str:
    file_path = f"./codeforces/{contest_id}{index}.json"
    if (os.path.exists(file_path)):
        print(f"{file_path} already exists.")
        return
    
    with open("./codeforces/failure.txt", "r") as file:
        if (f"{contest_id}{index}\n" in file):
            print(f"Already attempted to fetch problem {contest_id}{index}.")   
            return

    url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    headers = {"user-agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch problem details from Codeforces. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    dic = dict()
    dic["rating"] = rating
    dic["title"] = soup.find("div", class_="title").get_text(strip=True).split(" ", 1)[1]
    dic["time_limit"] = soup.find("div", class_="time-limit").get_text(separator=": ", strip=True)
    dic["memory_limit"] = soup.find("div", class_="memory-limit").get_text(separator=": ", strip=True)
    dic["problem_statement"] = ''.join([i for i in soup.find('div', 'header').next_sibling.get_text()])
    dic["input_spec"] = soup.find("div", class_="input-specification").get_text(separator="\n", strip=True)
    dic["output_spec"] = soup.find("div", class_="output-specification").get_text(separator="\n", strip=True)
    dic["examples"] = soup.find("div", class_="sample-test").get_text(separator="\n", strip=True)
    dic["notes"] = soup.find("div", class_="note").get_text(separator="\n", strip=True) if soup.find("div", class_="note") else ""
    try:
        blog_url = soup.find(lambda tag: tag.name == "a" and "Tutorial" in tag.text)["href"]
        dic["tutorial"] = fetch_tutorial(blog_url)
    except Exception as e:
        print(f"Fail to fetch tutorial {contest_id}{index}: {e}")
        dic["tutorial"] = "None"

    with open(file_path, "w") as file:
        json.dump(dic, file)

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
        if ("interactive" in problem["tags"]):
            continue
        try:
            if (problem.get("rating")):
                fetch_problem_details(problem["contestId"], problem["index"], problem["rating"])
            else:
                print(f"Problem {problem["contestId"]}{problem["index"]} didn't has rating.")
        except Exception as e:
            print(f'Fail to fetch problem {problem["contestId"]}{problem["index"]}: {e}')
            with open("./codeforces/failure.txt", "a") as file:
                file.write(f"{problem["contestId"]}{problem["index"]}\n")

def update_index():
    url = f"https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch problems from Codeforces API. Status code: {response.status_code}")

    response = response.json()
    if (response["status"] != "OK"):
        raise Exception(f'status: {response["status"]}\ncomment:{response["comment"]}')

    table = dict()
    problems = response["result"]["problems"]
    for problem in problems:
        file_path = f"./codeforces/{problem["contestId"]}{problem["index"]}.json"
        if (not os.path.exists(file_path)):
            continue
        for tag in problem["tags"]:
            if (tag not in table):
                table[tag] = list()
            table[tag].append(f"{problem["contestId"]}{problem["index"]}")

    with open("./codeforces/index.json", "w") as file:
        json.dump(table, file)

def build_training_set(num: int):
    from random import sample
    import glob
    import shutil

    directory_path = "./codeforces"
    json_files = glob.glob(os.path.join(directory_path, "*.json"))
    files = sample(json_files, num)
    for src in files:
        dest = src.replace("codeforces", "sample")
        shutil.copy(src, dest)

def add_rating():
    url = f"https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch problems from Codeforces API. Status code: {response.status_code}")

    response = response.json()
    if (response["status"] != "OK"):
        raise Exception(f'status: {response["status"]}\ncomment:{response["comment"]}')
    
    problems = response["result"]["problems"]
    for problem in problems:
        contest_id = problem["contestId"]
        index = problem["index"]
        file_path = f"./codeforces/{contest_id}{index}.json"
        if (not os.path.exists(file_path)):
            continue

        if (not problem.get("rating") or "special" in problem["tags"]):
            os.remove(file_path)
            print(f"{file_path} was removed.")
            continue
        
        with open(file_path, "r") as file:
            data = json.load(file)

        data["rating"] = problem["rating"]

        with open(file_path, "w") as file:
            json.dump(data, file)

if __name__ == "__main__":
    # update_problems()
    # update_index()
    build_training_set(1000)