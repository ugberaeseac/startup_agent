from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import AgentTool, ToolContext
from google.adk.code_executors import BuiltInCodeExecutor

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
    description='',
    instruction=
    """

    You are responsible for delegating tasks to the following agents:
    - competitior_agent


    You also have access to the following tools:
    - research_agent
    
    """
    tools=[AgentTool(agent=research_agent)]
)
