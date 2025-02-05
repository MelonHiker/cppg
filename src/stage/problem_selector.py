from src.configs.config_loader import settings
from litellm import completion

def select_problem(problems: list, min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story: str, logger) -> str:
    problems = "\n".join(problems)
    system_prompt = settings.problem_selector_prompt.system
    user_prompt = settings.problem_selector_prompt.user.format(min_difficulty=min_difficulty, max_difficulty=max_difficulty, skill_1=skill_1, skill_2=skill_2, problems=problems, story=story)
    
    logger.info(user_prompt)

    response = completion(
        model=settings.model,
        temperature=settings.problem_selector_prompt.temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    content = response.choices[0].message.content
    
    logger.info(content)
    return content