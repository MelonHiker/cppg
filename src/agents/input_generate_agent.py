from src.configs.config_loader import settings
from llama_index.llms.gemini import Gemini
from src.tools.llm_parser import LLMParser

async def generate_input(report: str, sample_input: str) -> str:
    config = settings.input_generate_agent
    prompt = config.prompt_tmpl.format(
        report=report,
        sample_input=sample_input
    )
    llm = Gemini(
        model=config.model,
        temperature=config.temperature
    )
    response = await llm.acomplete(prompt)
    parser = LLMParser()
    return parser.load_code(response.text, "python")