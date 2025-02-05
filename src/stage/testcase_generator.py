from src.configs.config_loader import settings
from litellm import completion

def testcase_generator(problem: dict, logger) -> str:
    sample_input = []
    for example in problem["examples"]:
        sample_input.append(example["input"])

    system_prompt = settings.testcase_generator_prompt.system
    user_prompt = settings.testcase_generator_prompt.user.format(
        problem=problem['description'],
        sample_input="=====".join(sample_input),
        input_constraints=problem['input_constraints'],
    )

    logger.info(user_prompt)

    response = completion(
        model=settings.model,
        temperature=settings.testcase_generator_prompt.temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    content = response.choices[0].message.content

    logger.info(content)
    
    return content