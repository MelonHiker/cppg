from src.configs.config_loader import settings
from llama_index.llms.gemini import Gemini

async def detail_craft(statement: str, story: str) -> str:
    config = settings.detail_craft_agent
    prompt = config.prompt_tmpl.format(problem_statement=statement, story=story)
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )
    response = await llm.acomplete(prompt)
    return response.text