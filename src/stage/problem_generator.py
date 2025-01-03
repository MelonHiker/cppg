from src.stage.random_problem import get_random_problems
from src.configs.config_loader import settings
from litellm import completion
from src.log import setup_logger

logger = setup_logger()
def generate_problem(min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story: str="") -> str:
    example_1 = get_random_problems(3, min_difficulty, max_difficulty, skill_1)
    example_2 = get_random_problems(3, min_difficulty, max_difficulty, skill_2, skill_1)
    system_prompt = settings.problem_generator_prompt.system
    user_prompt = settings.problem_generator_prompt.user.format(min_difficulty=min_difficulty, max_difficulty=max_difficulty, skill_1=skill_1, skill_2=skill_2, example_1=example_1, example_2=example_2, story=story)

    logger.info(user_prompt)

    response = completion(
    model=settings.model,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]
    )
    content = response.choices[0].message.content

    logger.info(content)

    return content
    
if __name__ == "__main__":
    import os
    os.environ["GEMINI_API_KEY"] = settings.api_key
    res = generate_problem("dp", "binary search")