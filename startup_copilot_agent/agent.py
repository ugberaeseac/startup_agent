from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import AgentTool, ToolContext
from google.adk.code_executors import BuiltInCodeExecutor

from .sub_agents.competitor_agent.agent import competitor_agent
from .sub_agents.marketsize_agent.agent import marketsize_agent
from .sub_agents.persona_agent.agent import persona_agent
from .sub_agents.pricing_agent.agent import pricing_agent
from .sub_agents.pitchdeck_agent.agent import pitchdeck_agent
from .sub_agents.research_agent.agent import research_agent



retry_config  = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)


root_agent = LlmAgent(
    name='startup_copilot_agent',
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=retry_config
    ),
    description=
    """
    Startup Copilot Root Agent. Orchestrates all sub-agents to guide founders from idea validation
    to business planning and pitch readiness. Receives founder queries about startup ideas and
    delegates tasks to sub-agents, including competitor analysis, market sizing, customer personas,
    and pricing strategy. Accesses the Research Agent for real-time data.
    Produces structured, actionable insights in a format ready for downstream use or iteration.
    """,
    instruction=
    """
    You are the Root Agent for Startup Copilot.

    Your role is to orchestrate all sub-agents and produce a detailed, professional, end-to-end startup analysis.

    You must ALWAYS run the following agents in order:
        1. research_agent → real-time research
        2. competitor_agent → competitor analysis
        3. marketsize_agent → TAM/SAM/SOM
        4. persona_agent → customer personas
        5. pricing_agent → pricing strategy
        6. pitchdeck_agent → pitch deck narrative

    After each agent runs, store the output in `output_key` using this structure:

    {
    "research": {},
    "competitors": {},
    "market_size": {},
    "personas": {},
    "pricing": {},
    "pitch_deck": {}
    }

    When all agents have completed:
    -   Read all collected outputs from `output_key`
    -   Produce ONE unified, investor-ready startup analysis that includes:
    -   Executive summary
    -   Competitor analysis
    -   Market sizing
    -   Personas
    -   Pricing strategy
    -   Pitch deck narrative

    Rules:
    - Do NOT insert placeholders or template variables.
    - Pull information directly from `output_key` after all agents finish.
    - The final output must be a polished, structured, human-readable document.

    """,
    #sub_agents=[competitor_agent, marketsize_agent, persona_agent, pricing_agent, pitchdeck_agent],
    tools=[
        AgentTool(research_agent), 
        AgentTool(competitor_agent), 
        AgentTool(marketsize_agent), 
        AgentTool(persona_agent), 
        AgentTool(pricing_agent), 
        AgentTool(pitchdeck_agent)
        ]
)
