from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    Event,
    step,
)
from src.tools.code_executor import CodeExecutor
from src.agents.problem_solve_agent import solve_problem
from src.agents.code_debug_agent import debug_code

class TestEvent(Event):
    code: str

class DebugEvent(Event):
    code: str
    error: str

class GenSolutionWorkflow(Workflow):
    def __init__(self, problem: dict, language: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.problem = problem
        self.language = language
        self.excutor = CodeExecutor()

    @step
    async def problem_solve(self, ev: StartEvent) -> TestEvent:
        code = await solve_problem(self.problem, self.language)
        return TestEvent(code=code)
    
    @step
    async def code_test(self, ev: TestEvent) -> StopEvent | DebugEvent:
        result = self.excutor.run_sample_tests(ev.code, self.language, self.problem["examples"])
        if (result == "Accept"):
            return StopEvent(result=ev.code)
        return DebugEvent(code=ev.code, error=result)

    @step
    async def code_debug(self, ev: DebugEvent) -> TestEvent:
        code = await debug_code(self.problem, ev.code, ev.error, self.language)
        return TestEvent(code=code)