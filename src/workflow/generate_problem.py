from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    Context,
    Event,
    step,
)
from src.agents.problem_forge_agent import forge_problem
from src.agents.detail_craft_agent import detail_craft
from src.agents.problem_validate_agent import validate_problem
from src.agents.reflection_agent import reflect_problem
from src.agents.reflection_validate_agent import validate_reflection
from src.tools.llm_parser import LLMParser
from build.rag_builder import RAGBuilder

class ForgeEvent(Event):
    pass

class PREvent(Event):
    statement: str
    similarity: int
    difficulty: int

class DetailCraftEvent(Event):
    statement: str

class ProblemValidateEvent(Event):
    problem: str

class ReflectionEvent(Event):
    problem: str

class ReflectionValidateEvent(Event):
    problem: str
    reflection: str

NUMBER_OF_SAMPLE = 5

class GenProblemWorkflow(Workflow):
    def __init__(self, min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query_engine = RAGBuilder().build_query_engine()
        self.parser = LLMParser()
        self.min_difficulty = min_difficulty
        self.max_difficulty = max_difficulty
        self.skill_1 = skill_1
        self.skill_2 = skill_2
        self.story = story

    @step
    async def start(self, ctx: Context, ev: StartEvent) -> ForgeEvent:
        for _ in range(NUMBER_OF_SAMPLE):
            ctx.send_event(ForgeEvent())

    @step(num_workers=NUMBER_OF_SAMPLE)
    async def problem_forge(self, ev: ForgeEvent) -> PREvent:
        problem = await forge_problem(self.min_difficulty, self.max_difficulty, self.skill_1, self.skill_2)
        response = await self.query_engine.aquery(problem["statement"])
        result = self.parser.load_yaml(str(response))
        if (not isinstance(result["similarity"], int) or not isinstance(result["difficulty"], int)):
            result["similarity"] = int(result["similarity"])
            result["difficulty"] = int(result["difficulty"])
        return PREvent(statement=problem["statement"], similarity=result["similarity"], difficulty=result["difficulty"])
    
    @step
    async def pointwise_ranking(self, ctx: Context, ev: PREvent) -> DetailCraftEvent | StartEvent:
        problems = ctx.collect_events(ev, [PREvent] * NUMBER_OF_SAMPLE)
        if problems is None:
            return None
        problems = [x for x in problems if self.min_difficulty <= x.difficulty <= self.max_difficulty]
        if (problems == []):
            return StartEvent()
        problems.sort(key=lambda x: (x.similarity, -x.difficulty))
        return DetailCraftEvent(statement=problems[0].statement)
    
    @step
    async def problem_detail_craft(self, ev: DetailCraftEvent) -> ProblemValidateEvent:
        result = await detail_craft(ev.statement, self.story)
        return ProblemValidateEvent(problem=result)
    
    @step
    async def problem_validate(self, ev: ProblemValidateEvent) -> ReflectionEvent:
        result = await validate_problem(ev.problem)
        return ReflectionEvent(problem=result["problem"])
    
    @step
    async def reflection(self, ev: ReflectionEvent) -> ReflectionValidateEvent:
        result = await reflect_problem(ev.problem)
        return ReflectionValidateEvent(problem=ev.problem, reflection=result)
    
    @step
    async def reflection_validate(self, ev: ReflectionValidateEvent) -> StopEvent:
        result = await validate_reflection(ev.problem, ev.reflection, self.skill_1, self.skill_2)
        return StopEvent(result=result)


if __name__ == "__main__":
    async def main(min_difficulty: int, max_difficulty: int, skill_1: str, skill_2: str, story: str=""):
        workflow = GenProblemWorkflow(min_difficulty, max_difficulty, skill_1, skill_2, story, timeout=300, verbose=True)
        result = await workflow.run()
        return result

    import os
    from phoenix.otel import register
    from src.configs.config_loader import settings

    os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY

    # Add Phoenix API Key for tracing
    os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={settings.PHOENIX_API_KEY}"
    os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"

    # configure the Phoenix tracer
    tracer_provider = register(
        project_name="cppg",
        set_global_tracer_provider=False
    )

    from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
    LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

    import asyncio
    min_difficulty = 1500
    max_difficulty = 2000
    skill_1 = "dp"
    skill_2 = "binary search"
    story = "MelonWaler ate a cat."
    response = asyncio.run(main(min_difficulty, max_difficulty, skill_1, skill_2, story))
    print(response)