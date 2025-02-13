from src.configs.config_loader import settings
from llama_index.llms.gemini import Gemini

async def reflect_problem(problem: dict) -> str:
    config = settings.reflection_agent
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
    )
    response = await llm.acomplete(prompt)
    return response.text