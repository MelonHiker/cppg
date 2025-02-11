from src.configs.config_loader import settings
from llama_index.llms.gemini import Gemini

async def analysis_input(problem: dict, sample_input: str):
    config = settings.input_analysis_agent
    prompt = config.prompt_tmpl.format(
        problem=problem['description'],
        input_constraints=problem['input_constraints'],
        sample_input=sample_input
    )
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )
    response = await llm.acomplete(prompt)
    return response.text