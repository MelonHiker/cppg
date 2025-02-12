from src.tools.random_problem import get_random_problems
from src.configs.config_loader import settings
from src.tools.llm_parser import LLMParser
from llama_index.llms.gemini import Gemini

async def forge_problem(min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str) -> dict:
    problems_1 = get_random_problems(5, min_difficulty, max_difficulty, skill_1, None)
    problems_2 = get_random_problems(5, min_difficulty, max_difficulty, skill_2, skill_1)

    example_1 = ""
    for problem in problems_1:
        example_1 += f"difficulty: {problem['rating']}\n"
        example_1 += problem["problem_statement"]
        example_1 += "\n\n---\n\n"
    
    example_2 = ""
    for problem in problems_2:
        example_2 += f"difficulty: {problem['rating']}\n"
        example_2 += problem["problem_statement"]
        example_2 += "\n\n---\n\n"
    
    config = settings.problem_forge_agent
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )

    prompt = config.prompt_tmpl.format(
        min_difficulty=min_difficulty,
        max_difficulty=max_difficulty,
        skill_1=skill_1, 
        skill_2=skill_2,
        example_1=example_1,
        example_2=example_2
    )

    response = await llm.acomplete(prompt)
    parser = LLMParser()
    keys = ["statement", "explains"]
    return parser.load_yaml(response.text, keys)