from src.configs.config_loader import settings
from litellm import completion

def debug(problem: dict, code: str, error: str, language: str, logger):
    system_prompt = settings.code_debugger_prompt.system
    user_prompt = settings.code_debugger_prompt.user.format(
        tags=", ".join(problem['tags']),
        problem=problem['description'],
        time_limit=problem['time_limit'],
        memory_limit=problem['memory_limit'],
        input_constraints=problem['input_constraints'],
        output_constraints=problem['output_constraints'],
        tutorial=problem['solution_in_natural_language'],
        code=code,
        error=error,
        language=language
    )

    logger.info(user_prompt)

    response = completion(
        model=settings.model,
        temperature=settings.code_debugger_prompt.temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    content = response.choices[0].message.content

    logger.info(content)
    
    return content