from src.configs.config_loader import settings
from llama_index.llms.gemini import Gemini
from src.tools.llm_parser import LLMParser

async def debug_code(problem: dict, code: str, error: str, language: str):
    config = settings.code_debug_agent
    prompt = config.prompt_tmpl.format(
        tags=", ".join(problem['tags']),
        problem=problem['description'],
        time_limit=problem['time_limit'],
        memory_limit=problem['memory_limit'],
        input_specifications=problem['input_specifications'],
        output_specifications=problem['output_specifications'],
        tutorial=problem['solution_explanation'],
        code=code,
        error=error,
        language=language
    )
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )
    response = await llm.acomplete(prompt)
    parser = LLMParser()
    return parser.load_code(response.text, language)
