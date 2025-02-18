from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    Event,
    step,
)
from llama_index.core.workflow.retry_policy import ConstantDelayRetryPolicy
from src.agents.reflection_agent import reflect_problem
from src.agents.reflection_validate_agent import validate_reflection

class ReflectionValidateEvent(Event):
    problem: dict
    reflection: str

class GenReflectionWorkflow(Workflow):
    @step
    async def reflection(self, ev: StartEvent) -> ReflectionValidateEvent:
        result = await reflect_problem(ev.problem)
        return ReflectionValidateEvent(problem=ev.problem, reflection=result)
    
    @step(retry_policy=ConstantDelayRetryPolicy(delay=5, maximum_attempts=3))
    async def reflection_validate(self, ev: ReflectionValidateEvent) -> StopEvent:
        result = await validate_reflection(ev.problem, ev.reflection)
        return StopEvent(result=result)