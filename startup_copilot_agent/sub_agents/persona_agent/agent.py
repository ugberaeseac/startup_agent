from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search, AgentTool, ToolContext
from google.adk.code_executors import BuiltInCodeExecutor



retry_config  = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)


persona_agent = LlmAgent(
    name='persona_agent',
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=retry_config
    ),
    description=
    """
    Persona Agent for Startup Copilot. Creates detailed customer personas for a startup idea to help
    founders understand target audiences and design products and marketing strategies.
    """,
    instruction=
    """
    You are the Persona Agent. Your task is to generate customer personas for a startup idea.

    Output Requirements:

    Return structured JSON with fields:
    -   persona_name
    -   age_range
    -   location
    -   occupation
    -   pain_points
    -   goals
    -   behaviors

    Ensure personas are realistic, concise, and actionable for product and marketing decisions
    """,
    output_key='user_personas'
)