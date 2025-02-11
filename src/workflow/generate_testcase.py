from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    Event,
    step,
)
from src.agents.input_analysis_agent import analysis_input
from src.agents.input_generate_agent import generate_input

class CodeEvent(Event):
    report: str
    sample_input: str

class GenTestWorkflow(Workflow):
    def __init__(self, problem: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.problem = problem

    @step
    async def input_analysis(self, ev: StartEvent) -> CodeEvent:
        sample_input = []
        for example in self.problem["examples"]:
            sample_input.append(example["input"])
        sample_input = "\n---\n".join(sample_input)
        result = await analysis_input(self.problem, sample_input)
        return CodeEvent(report=result, sample_input=sample_input)
    
    @step
    async def input_generate(self, ev: CodeEvent) -> StopEvent:
        code = await generate_input(ev.report, ev.sample_input)
        return StopEvent(result=code)