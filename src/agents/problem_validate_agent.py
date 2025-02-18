from src.configs.config_loader import settings
from llama_index.llms.gemini import Gemini
from src.tools.llm_parser import LLMParser

async def validate_problem(problem: str, tags: list[str]) -> dict:
    config = settings.problem_validate_agent
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )
    prompt = config.prompt_tmpl.format(
        problem=problem,
    )
    response = await llm.acomplete(prompt)
    parser = LLMParser()
    keys = [
        "title", 
        "time_limit", 
        "memory_limit", 
        "description", 
        "input_specifications", 
        "output_specifications", 
        "examples", 
        "note", 
        "explanation"
    ]
    result = parser.load_yaml(response.text, keys)
    result["tags"] = tags
    return result