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


if __name__ == "__main__":
    async def main(problem: str) -> str:
        workflow = GenTestWorkflow(problem, timeout=120, verbose=True)
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
    problem = {"result":{"title":"Deadline Driven Projects","time_limit":"1 second","memory_limit":"256 megabytes","description":"MelonWaler, after a peculiar morning involving a cat and a questionable breakfast choice, found himself strangely motivated to manage projects.  His company is planning to undertake several projects. There are $n$ projects, and the $i$-th project has a profit $p_i$, a resource requirement $r_i$, and a deadline $d_i$. To receive the profit $p_i$ from project $i$, it must be completed by day $d_i$.\n\nThe company has a total resource budget of $B$. They want to achieve a total profit of at least $P$.  Your task is to determine the minimum possible global deadline $D$ such that it is possible to select a subset of projects and complete them. For a selected project $i$, it must be completed by both its individual deadline $d_i$ and the global deadline $D$.  The total resource cost for all selected projects must not exceed the budget $B$, and the sum of profits of selected projects must be at least $P$.\n\nIf it is impossible to achieve the target profit $P$ even with a very large global deadline, you should output $-1$.","input_constraints":"- The first line contains three integers $n$, $B$, and $P$ ($1 \\le n \\le 100$, $1 \\le B \\le 10^5$, $1 \\le P \\le 10^9$), representing the number of projects, the total resource budget, and the target profit, respectively.\n- The next $n$ lines describe the projects. The $i$-th line contains three integers $p_i$, $r_i$, and $d_i$ ($1 \\le p_i \\le 10^9$, $1 \\le r_i \\le 10^3$, $1 \\le d_i \\le 10^5$), representing the profit, resource requirement, and deadline of the $i$-th project, respectively.","output_constraints":"- Output a single integer, representing the minimum possible global deadline $D$. If it is impossible to achieve the target profit $P$, output $-1$.","examples":[{"input":"2 15 10\n5 10 2\n8 5 3","output":"3"},{"input":"3 12 15\n10 10 1\n5 5 2\n7 8 3","output":"-1"},{"input":"3 18 15\n10 10 1\n5 5 2\n7 8 3","output":"2"}],"note":"In the first example, with a global deadline $D=3$, we can select both projects. Project 1 and Project 2 are both completable within the global deadline $D=3$ and their individual deadlines $d_1=2$ and $d_2=3$ respectively. The total profit is $5+8=13 \\ge 10$, and the total resource cost is $10+5=15 \\le 15$. If we try a smaller global deadline $D=2$, we can only select project 1. The profit is $5 < 10$, so we cannot achieve the target profit. Thus, the minimum global deadline is $3$.\n\nIn the second example, even if we consider all projects and set a very large global deadline, the maximum achievable profit is $10+7=17$ (by selecting project 1 and 3, but resource cost $10+8=18 > 12$, so we cannot select both. If we select project 1 and 2, profit $10+5=15$, resource cost $10+5=15 > 12$. If we select project 2 and 3, profit $5+7=12 < 15$. If we only select project 1, profit $10 < 15$. If we only select project 2, profit $5 < 15$. If we only select project 3, profit $7 < 15$. The maximum profit we can achieve within the budget is $10$ (by selecting project 1) or $7$ (by selecting project 3) or $5$ (by selecting project 2). In any case, it is less than $15$. Therefore, it is impossible to achieve the target profit, and the output is $-1$.\n\nIn the third example, with a global deadline $D=2$, we can select project 1 and project 2. Both are completable within $D=2$ and their individual deadlines. The total profit is $10+5=15 \\ge 15$, and the total resource cost is $10+5=15 \\le 18$. If we try a smaller global deadline $D=1$, we can only select project 1. The profit is $10 < 15$. Thus, the minimum global deadline is $2$.","solution_in_natural_language":"The problem asks for the minimum global deadline $D$ to achieve a target profit $P$ within a resource budget $B$. We can use binary search to find the minimum $D$. For a given $D$, we need to check if it's possible to achieve profit $P$. To check this, we consider only the projects whose individual deadlines are less than or equal to $D$. Among these projects, we want to select a subset such that the total resource cost is within $B$ and the total profit is at least $P$. This selection problem can be solved using dynamic programming, which is a variation of the 0/1 knapsack problem.\n\nFirst, we need to determine if it's even possible to reach the target profit $P$ regardless of deadlines. We can use dynamic programming to find the maximum profit achievable within the budget $B$ using all projects. If this maximum profit is less than $P$, then it's impossible to achieve the target, and we should output $-1$.\n\nIf it is possible to achieve the target profit, we can perform a binary search for the minimum global deadline $D$. We can search in the range from 1 to the maximum individual deadline among all projects. For each value of $D$ in the binary search, we filter out projects whose individual deadline $d_i$ is greater than $D$. Then, using the remaining projects, we use dynamic programming to find the maximum profit we can achieve within the resource budget $B$. If this maximum profit is at least $P$, then $D$ is a feasible global deadline, and we try to find a smaller $D$. Otherwise, $D$ is not feasible, and we need to try a larger $D$. The binary search will converge to the minimum feasible global deadline.\n\nThe dynamic programming state can be defined as $dp[i][j]$, which represents the maximum profit that can be achieved using the first $i$ available projects (after filtering based on the global deadline $D$) with a resource budget of $j$. The transition is as follows: either we don't include the $i$-th project, in which case $dp[i][j] = dp[i-1][j]$, or we include the $i$-th project (if its resource requirement $r_i$ is less than or equal to $j$), in which case $dp[i][j] = p_i + dp[i-1][j-r_i]$. We take the maximum of these two options.\n\nThe overall algorithm is:\n1. Perform an initial check using dynamic programming to see if the target profit $P$ is achievable at all within budget $B$, ignoring deadlines. If not, output $-1$.\n2. Binary search for the global deadline $D$. For each candidate $D$:\n   a. Filter projects to include only those with individual deadlines $d_i \\le D$.\n   b. Use dynamic programming to find the maximum profit achievable from these filtered projects within budget $B$.\n   c. If the maximum profit is at least $P$, then $D$ is feasible, so try a smaller $D$. Otherwise, try a larger $D$.\n3. Output the minimum feasible $D$ found by binary search.","time_complexity":"The time complexity of the initial feasibility check using dynamic programming is $O(n \\cdot B)$.\nFor each iteration of the binary search, we filter projects in $O(n)$ time and then perform dynamic programming in $O(n \\cdot B)$ time in the worst case (if all projects are filtered). The binary search runs for $O(\\log(\\max(d_i)))$ iterations.\nTherefore, the total time complexity is $O(n \\cdot B + \\log(\\max(d_i)) \\cdot (n + n \\cdot B)) = O(n \\cdot B \\cdot \\log(\\max(d_i)))$.","space_complexity":"The space complexity is dominated by the dynamic programming tables, which are of size $O(n \\cdot B)$. Thus, the space complexity is $O(n \\cdot B)$.","tags":"- dp\n- binary search","explanation":"**Example 1 Explanation:**\nFor the first example, we have projects: Project 1 (profit=5, resource=10, deadline=2), Project 2 (profit=8, resource=5, deadline=3), budget $B=15$, and target profit $P=10$.\n- If we set a global deadline $D=2$, only Project 1 is valid (deadline $d_1=2 \\le 2$). We can select Project 1, with profit 5 and resource 10. Total profit is 5, which is less than 10. So $D=2$ is not sufficient.\n- If we set a global deadline $D=3$, both Project 1 and Project 2 are valid (deadlines $d_1=2 \\le 3$, $d_2=3 \\le 3$). We can select both projects. Total profit is $5+8=13$, which is greater than or equal to 10. Total resource cost is $10+5=15$, which is less than or equal to 15. So $D=3$ is sufficient.\nSince $D=2$ is not sufficient and $D=3$ is sufficient, the minimum global deadline is 3.\n\n**Example 2 Explanation:**\nFor the second example, projects are: Project 1 (profit=10, resource=10, deadline=1), Project 2 (profit=5, resource=5, deadline=2), Project 3 (profit=7, resource=8, deadline=3), budget $B=12$, and target profit $P=15$.\nLet's consider all possible combinations of projects within the budget $B=12$:\n- Project 1: profit 10, resource 10.\n- Project 2: profit 5, resource 5.\n- Project 3: profit 7, resource 8.\n- Project 1 + Project 2: resource $10+5=15 > 12$ (invalid).\n- Project 1 + Project 3: resource $10+8=18 > 12$ (invalid).\n- Project 2 + Project 3: resource $5+8=13 > 12$ (invalid).\nThe maximum profit we can get is by selecting either Project 1 (profit 10) or Project 3 (profit 7) or Project 2 (profit 5). In all cases, the maximum profit is $\\max(10, 7, 5) = 10$, which is less than the target profit $P=15$. Therefore, it's impossible to achieve the target profit, and the output is -1.\n\n**Example 3 Explanation:**\nFor the third example, projects are: Project 1 (profit=10, resource=10, deadline=1), Project 2 (profit=5, resource=5, deadline=2), Project 3 (profit=7, resource=8, deadline=3), budget $B=18$, and target profit $P=15$.\n- If we set a global deadline $D=1$, only Project 1 is valid. Profit = 10 < 15. Not enough.\n- If we set a global deadline $D=2$, Projects 1 and 2 are valid. We can select both. Total profit $10+5=15 \\ge 15$. Total resource $10+5=15 \\le 18$. So $D=2$ is sufficient.\nSince $D=1$ is not sufficient and $D=2$ is sufficient, the minimum global deadline is 2."}}
    response = asyncio.run(main(problem["result"]))
    print(response)