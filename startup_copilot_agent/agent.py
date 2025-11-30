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
    Startup Copilot Root Agent. Serves as the manager and orchestrator of all sub-agents. 
    Receives user queries related to building a startup, and delegates tasks to the appropriate
    sub-agent (Competitor, Market Size, Persona, Pricing) to generate structured insights. 
    Has access to the Research Agent as a tool for gathering real-time information.
    """,
    instruction=
    """
    You are the Root Agent for Startup Copilot. Your responsibility is to understand the user's request
    and delegate tasks to the appropriate sub-agent:

    -   If the user asks about competitors, delegate to competitor_agent.
    -   If the user asks about market size, delegate to marketsize_agent.
    -   If the user asks about customer personas, delegate to persona_agent.
    -   If the user asks about pricing strategies, delegate to pricing_agent.
    
    You also have access to research_agent as a tool for gathering real-time data.

    Output Requirements:

    -   Collect and return outputs from sub-agents in a structured JSON format.
    -   Ensure each sub-agent's output is labeled clearly (e.g., competitors, market_size, persona, pricing).
    -   If the user query requires multiple sub-agents, delegate to each sequentially and aggregate results.
    -   Keep responses concise and actionable, suitable for use in a startup planning workflow.
    
    """,
    tools=[AgentTool(agent=research_agent)]
)
