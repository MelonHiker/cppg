from src.configs.config_loader import settings
from src.tools.llm_parser import LLMParser
from llama_index.llms.gemini import Gemini

async def validate_reflection(problem: dict, reflection: str) -> dict:
    config = settings.reflection_validate_agent
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )
    prompt = config.prompt_tmpl.format(
        problem=problem['description'],
        sample_IO=problem['examples'],
        time_limit=problem['time_limit'],
        memory_limit=problem['memory_limit'],
        input_specifications=problem['input_specifications'],
        output_specifications=problem['output_specifications'],
        reflection=reflection,
    )
    response = await llm.acomplete(prompt)
    parser = LLMParser()
    keys = [
        "solution_explanation", 
        "time_complexity", 
        "space_complexity", 
        "explanation"
    ]
    return parser.load_yaml(response.text, keys)