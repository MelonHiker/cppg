from src.configs.config_loader import settings
from src.tools.llm_parser import LLMParser
from llama_index.llms.gemini import Gemini

async def validate_reflection(problem: str, reflection: str, skill_1: str, skill_2: str) -> dict:
    config = settings.reflection_validate_agent
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )
    prompt = config.prompt_tmpl.format(
        problem=problem,
        reflection=reflection,
        skill_1=skill_1,
        skill_2=skill_2
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
        "solution_in_natural_language", 
        "time_complexity", 
        "space_complexity", 
        "tags",
        "explanation"
    ]
    return parser.load_yaml(response.text, keys)