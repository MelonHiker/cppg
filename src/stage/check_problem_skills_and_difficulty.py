from src.configs.config_loader import settings
from src.log import setup_logger
from litellm import completion

logger = setup_logger()
def check_skills_difficulty(min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, problem: str) -> str:
    system_prompt = settings.check_problem_skills_and_difficulty_prompt.system
    user_prompt = settings.check_problem_skills_and_difficulty_prompt.user.format(min_difficulty=min_difficulty, max_difficulty=max_difficulty, skill_1=skill_1, skill_2=skill_2, problem=problem)
    
    logger.info(user_prompt)

    response = completion(
    model=settings.model,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]
    )
    content = response.choices[0].message.content
    
    logger.info(content)
    return content.find("yes") != -1