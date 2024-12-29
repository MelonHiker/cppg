from src.configs.config_loader import settings
from src.log import setup_logger
from litellm import completion

logger = setup_logger()
def reflect_problem(problem: str) -> str:
    system_prompt = settings.problem_reflection_prompt.system
    user_prompt = settings.problem_reflection_prompt.user.format(problem=problem)
    
    logger.info(user_prompt)

    response = completion(
    model=settings.model,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]
    )
    content = response.choices[0].message.content

    logger.info(content)
    
    return content