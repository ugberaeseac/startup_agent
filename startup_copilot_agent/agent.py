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
    You are the Root Agent for the Startup Copilot. Your role is to understand the founder's request and
    coordinate the workflow by delegating tasks to the appropriate sub-agents. You must NOT solve tasks yourself;
    always delegate.

    Your Responsibilities are to delegate tasks to the appropriate sub-agents:
    -   research_agent → Real-time research
    -   competitor_agent → Competitor analysis
    -   marketsize_agent → Market sizing
    -   persona_agent → Customer personas
    -   pricing_agent → Pricing strategy
    -   pitchdeck_agent → Pitch deck narrative
    
    You also have access to the following tools:
    -   research_agent

    Your responsibilities:

    1. Interpret the user's request and determine which sub-agents need to be called.
    2. Delegate tasks to sub-agents and gather their outputs.
    3. Store all sub-agent outputs in `output_key` using the following structure:
    
    {
    "research": {},
    "competitors": {},
    "market_size": {},
    "personas": {},
    "pricing": {},
    "pitch_deck": {}
    }

    4. Maintain session continuity by reusing prior outputs unless the user requests new analysis.
    5. Ensure all outputs are concise, structured, and actionable.
    6. If a sub-agent cannot find relevant data, store:
    { "status": "no_data" }
    7. Avoid commentary or motivational text. Focus only on orchestration and producing usable output.

    Goal: Deliver a unified, structured pipeline of startup insights by orchestrating all sub-agents effectively.
    """,
    sub_agents=[competitor_agent, marketsize_agent, persona_agent, pricing_agent, pitchdeck_agent],
    tools=[AgentTool(agent=research_agent)]
)
