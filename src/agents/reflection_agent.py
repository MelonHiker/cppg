from src.configs.config_loader import settings
from llama_index.llms.gemini import Gemini

async def reflect_problem(problem: str) -> str:
    config = settings.reflection_agent
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )
    prompt = config.prompt_tmpl.format(
        problem=problem,
    )
    response = await llm.acomplete(prompt)
    return response.text