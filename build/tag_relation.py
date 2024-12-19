import requests
import json
from pprint import pprint

tags = []
with open("tags.txt", "r", encoding="utf-8") as file:
    tags = file.read().splitlines()

tot_problems = {key: 0 for key in tags}
tag_similarity = dict()
for tag in tags:
    url = f"https://codeforces.com/api/problemset.problems?tags={tag}"
    problems = requests.get(url).json()["result"]["problems"]
    tot_problems[tag] = len(problems)
    cnt_tags = {key: 0 for key in tags if key != tag}
    for problem in problems:
        for other_tag in problem["tags"]:
            if (other_tag not in cnt_tags):
                continue
            cnt_tags[other_tag] += 1
    tag_similarity[tag] = cnt_tags

for tag in tags:
    for other_tag in tag_similarity[tag]:
        tag_similarity[tag][other_tag] /= tot_problems[other_tag]

low_similarity_tags = dict()
for tag in tags:
    low_similarity_tags[tag] = list()
    for other_tag, pct in tag_similarity[tag].items():
        if (pct < 0.3):
            low_similarity_tags[tag].append(other_tag)

with open("tag_relations.json", "w") as file:
    json.dump(low_similarity_tags, file)