from llama_index.core.workflow import (
    StartEvent,
    StopEvent,
    Workflow,
    Context,
    Event,
    step,
)
from llama_index.core.workflow.retry_policy import ConstantDelayRetryPolicy
from src.agents.problem_forge_agent import forge_problem
from src.agents.detail_craft_agent import detail_craft
from src.agents.problem_validate_agent import validate_problem
from src.tools.llm_parser import LLMParser
from build.rag_builder import RAGBuilder
from src.configs.config_loader import settings

class ForgeEvent(Event):
    pass

class PREvent(Event):
    statement: str
    similarity: int
    difficulty: int
    tags: list[str]

class DetailCraftEvent(Event):
    statement: str

class ProblemValidateEvent(Event):
    problem: str

config = settings.GenProblemWorkflow

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
        for _ in range(config.num_of_samples):
            ctx.send_event(ForgeEvent())

    @step(num_workers=config.num_of_workers, retry_policy=ConstantDelayRetryPolicy(delay=10, maximum_attempts=3))
    async def problem_forge(self, ev: ForgeEvent) -> PREvent:
        problem = await forge_problem(self.min_difficulty, self.max_difficulty, self.skill_1, self.skill_2)
        response = await self.query_engine.aquery(problem["statement"])
        result = self.parser.load_yaml(str(response))
        if (not isinstance(result["similarity"], int) or not isinstance(result["difficulty"], int)):
            result["similarity"] = int(result["similarity"])
            result["difficulty"] = int(result["difficulty"])
        return PREvent(statement=problem["statement"], similarity=result["similarity"], difficulty=result["difficulty"], tags=result["tags"])
    
    @step
    async def pointwise_ranking(self, ctx: Context, ev: PREvent) -> DetailCraftEvent | StartEvent:
        problems = ctx.collect_events(ev, [PREvent] * config.num_of_samples)
        if problems is None:
            return None
        problems = [
            x for x in problems
            if (self.min_difficulty <= x.difficulty <= self.max_difficulty)
            and (self.skill_1 in x.tags)
            and (self.skill_2 in x.tags)
        ]
        if (problems == []):
            return StartEvent()
        problems.sort(key=lambda x: (x.similarity, -x.difficulty))
        await ctx.set("tags", problems[0].tags)
        return DetailCraftEvent(statement=problems[0].statement)
    
    @step(retry_policy=ConstantDelayRetryPolicy(delay=5, maximum_attempts=3))
    async def problem_detail_craft(self, ev: DetailCraftEvent) -> ProblemValidateEvent:
        result = await detail_craft(ev.statement, self.story)
        return ProblemValidateEvent(problem=result)
    
    @step(retry_policy=ConstantDelayRetryPolicy(delay=5, maximum_attempts=3))
    async def problem_validate(self, ctx: Context, ev: ProblemValidateEvent) -> StopEvent:
        result = await validate_problem(ev.problem, await ctx.get("tags"))
        return StopEvent(result=result)