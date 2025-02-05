from src.configs.config_loader import settings
from litellm import completion

def validate_problem(min_difficulty: int, max_difficulty: int, problem: str, skill_1: str, skill_2: str, logger) -> str:
    system_prompt = settings.problem_validator_prompt.system
    user_prompt = settings.problem_validator_prompt.user.format(skill_1=skill_1, skill_2=skill_2, problem=problem, min_difficulty=min_difficulty, max_difficulty=max_difficulty)
    
    logger.info(user_prompt)

    response = completion(
        model=settings.model,
        temperature=settings.problem_validator_prompt.temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    content = response.choices[0].message.content
    
    logger.info(content)
    return content