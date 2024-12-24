from random import sample
from bs4 import BeautifulSoup
import requests

def get_random_problems(skill, count):
    url = f"https://codeforces.com/api/problemset.problems?tags={skill}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch problems from Codeforces API. Status code: {response.status_code}")

    problems = response.json().json()["result"]["problems"]
    if len(problems) < count:
        raise Exception("Not enough problems to choose from.")
    return sample(problems, count)

def get_problem_statement(contest_id, index):
    url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch problem details from Codeforces. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("div", class_="title").get_text(strip=True).split(" ", 1)[1]
    time_limit = soup.find("div", class_="time-limit").get_text(separator=": ", strip=True)
    memory_limit = soup.find("div", class_="memory-limit").get_text(separator=": ", strip=True)
    problem_statement = ''.join([i for i in soup.find('div', 'header').next_sibling.get_text()])
    input_spec = soup.find("div", class_="input-specification").get_text(separator="\n", strip=True)
    output_spec = soup.find("div", class_="output-specification").get_text(separator="\n", strip=True)
    examples = soup.find("div", class_="sample-test").get_text(separator="\n", strip=True)
    notes = soup.find("div", class_="note").get_text(separator="\n", strip=True) if soup.find("div", class_="note") else ""
    
    problem = f"{title}\n{time_limit}\n{memory_limit}\n\n{problem_statement}\n\n{input_spec}\n\n{output_spec}\n\nExample\n{examples}\n\n{notes}"
    return problem.strip()

if __name__ == "__main__":
    print(get_problem_statement(2035, "C"))