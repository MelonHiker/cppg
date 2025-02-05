from src.stage.random_problem import get_random_problems
from src.configs.config_loader import settings
from litellm import acompletion

async def generate_problem(min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, logger) -> str:
    problems_1 = get_random_problems(5, min_difficulty, max_difficulty, skill_1, None)
    problems_2 = get_random_problems(5, min_difficulty, max_difficulty, skill_2, skill_1)

    example_1 = ""
    for problem in problems_1:
        example_1 += f"difficulty: {problem['rating']}\n"
        example_1 += problem["problem_statement"]
        example_1 += "\n"
    
    example_2 = ""
    for problem in problems_2:
        example_2 += f"difficulty: {problem['rating']}\n"
        example_2 += problem["problem_statement"]
        example_2 += "\n"
        
    system_prompt = settings.problem_generator_prompt.system
    user_prompt = settings.problem_generator_prompt.user.format(min_difficulty=min_difficulty, max_difficulty=max_difficulty, skill_1=skill_1, skill_2=skill_2, example_1=example_1, example_2=example_2)

    logger.info(user_prompt)

    response = await acompletion(
        model=settings.model,
        temperature=settings.problem_generator_prompt.temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    content = response.choices[0].message.content

    logger.info(content)

    return content