from random_problem import get_random_problems
from configs.config_loader import settings
from litellm import completion
from log import setup_logger

logger = setup_logger()
def reflect_problem(problem: str) -> str:
    system_prompt = settings.problem_reflection_prompt.system
    user_prompt = settings.problem_reflection_prompt.user.format(problem=problem)
    response = completion(
    model=settings.model,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]
    )
    content = response.choices[0].message.content
    logger.info(content)
    return content