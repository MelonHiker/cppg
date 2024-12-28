from random_problem import get_random_problems
from configs.config_loader import settings
from litellm import completion
from log import setup_logger

logger = setup_logger()
def generate_problem(skill_1: str, skill_2: str, story: str="") -> str:
    example_1 = get_random_problems(3, skill_1)
    example_2 = get_random_problems(3, skill_2, skill_1)
    system_prompt = settings.generate_problem_prompt.system
    user_prompt = settings.generate_problem_prompt.user.format(skill_1=skill_1, skill_2=skill_2, example_1=example_1, example_2=example_2, story=story)

    logger.info(user_prompt)

    response = completion(
    model=settings.model,
    messages=[{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]
    )
    problem = response.choices[0].message.content

    logger.info(problem)

    return problem
    
if __name__ == "__main__":
    import os
    os.environ["GEMINI_API_KEY"] = settings.api_key
    res = generate_problem("dp", "binary search")