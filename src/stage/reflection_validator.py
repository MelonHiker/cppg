from src.log import setup_logger
from src.configs.config_loader import settings
from litellm import completion

def validate_reflection(problem: str, reflection: str, skill_1: str, skill_2: str, logger) -> str:
    system_prompt = settings.reflection_validator_prompt.system
    user_prompt = settings.reflection_validator_prompt.user.format(problem=problem, reflection=reflection, skill_1=skill_1, skill_2=skill_2)
    
    logger.info(user_prompt)
    
    response = completion(
                    model=settings.model,
                    messages=[{"role": "system", "content": system_prompt},
                              {"role": "user", "content": user_prompt}]
    )
    content = response.choices[0].message.content
    logger.info(content)

    return content