from src.configs.config_loader import settings
from litellm import completion

def solve_problem(problem: dict, language: str, logger) -> str:
    system_prompt = settings.problem_solver_prompt.system
    user_prompt = settings.problem_solver_prompt.user.format(
        tags=", ".join(problem['tags']),
        problem=problem['description'],
        sample_IO=problem['examples'],
        time_limit=problem['time_limit'],
        memory_limit=problem['memory_limit'],
        input_constraints=problem['input_constraints'],
        output_constraints=problem['output_constraints'],
        tutorial=problem['solution_in_natural_language'],
        language=language
    )

    logger.info(user_prompt)

    response = completion(
        model=settings.model,
        temperature=settings.problem_solver_prompt.temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    content = response.choices[0].message.content

    logger.info(content)
    
    return content