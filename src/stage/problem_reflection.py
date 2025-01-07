from src.configs.config_loader import settings
from litellm import completion

def reflect_problem(problem: str, logger) -> str:
    system_prompt = settings.problem_reflection_prompt.system
    user_prompt = settings.problem_reflection_prompt.user.format(problem=problem)
    
    logger.info(user_prompt)

    response = completion(
    model=settings.model,
    messages=[{"role": "system", "content": settings.thinking_gemini_prompt.system},
              {"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]
    )
    content = response.choices[0].message.content

    logger.info(content)
    
    return content