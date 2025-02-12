from src.configs.config_loader import settings
from llama_index.llms.gemini import Gemini
from src.tools.llm_parser import LLMParser

async def solve_problem(problem: dict, language: str) -> str:
    config = settings.problem_solve_agent
    prompt = config.prompt_tmpl.format(
        tags=", ".join(problem['tags']),
        problem=problem['description'],
        sample_IO=problem['examples'],
        time_limit=problem['time_limit'],
        memory_limit=problem['memory_limit'],
        input_specifications=problem['input_specifications'],
        output_specifications=problem['output_specifications'],
        tutorial=problem['solution_in_natural_language'],
        language=language
    )
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )
    response = await llm.acomplete(prompt)
    parser = LLMParser()
    return parser.load_code(response.text, language)