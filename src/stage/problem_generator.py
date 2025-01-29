from src.stage.random_problem import get_random_problems
from src.configs.config_loader import settings
from litellm import acompletion

async def generate_problem(min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story: str, logger) -> str:
    example_1 = get_random_problems(3, min_difficulty, max_difficulty, skill_1, None, logger)
    example_2 = get_random_problems(3, min_difficulty, max_difficulty, skill_2, skill_1, logger)
    system_prompt = settings.problem_generator_prompt.system
    user_prompt = settings.problem_generator_prompt.user.format(min_difficulty=min_difficulty, max_difficulty=max_difficulty, skill_1=skill_1, skill_2=skill_2, example_1=example_1, example_2=example_2, story=story)

    logger.info(user_prompt)

    response = await acompletion(
    model=settings.model,
    temperature=settings.problem_generator_prompt.temperature,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]
    )
    content = response.choices[0].message.content

    logger.info(content)

    return content