from src.configs.config_loader import settings
from src.log import setup_logger
from litellm import completion

logger = setup_logger()
def validate_problem(problem: str, skill_1: str, skill_2: str) -> str:
    system_prompt = settings.problem_validator_prompt.system
    user_prompt = settings.problem_validator_prompt.user.format(skill_1=skill_1, skill_2=skill_2, problem=problem)
    
    logger.info(user_prompt)

    response = completion(
    model=settings.model,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]
    )
    content = response.choices[0].message.content
    
    logger.info(content)
    return content