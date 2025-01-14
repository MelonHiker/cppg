from src.configs.config_loader import settings
from litellm import completion

def solve_problem(problem: str, language: str, logger) -> str:
    system_prompt = settings.problem_solver_prompt.system
    user_prompt = settings.problem_solver_prompt.user.format(problem=problem, language=language)
    
    logger.info(user_prompt)

    response = completion(
    model=settings.model,
    temperaturel=settings.problem_solver_prompt.temperature,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]
    )
    content = response.choices[0].message.content

    logger.info(content)
    
    return content