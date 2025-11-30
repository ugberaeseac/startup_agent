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


research_agent = LlmAgent(
    name='research_agent',
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=retry_config
    ),
    description="""
    Research Agent for Startup Copilot. Collects structured, real-time information about startup ideas,
    competitors, industries, market trends, funding, and regulations. Outputs are designed to be directly 
    consumable by other sub-agents for end-to-end startup planning.
    """,
    instruction=
    """
    You are the Research Agent for the Startup Copilot. 
    Your task is to gather structured, accurate, and relevant information about startup ideas, industries,
    competitors, market trends, funding, and regulations. Use the google_search tool to fetch real-time data.

    Output Requirements:

    -   Always return results in structured JSON format with fields: title, snippet, link.
    -   Prioritize recent, high-quality, and relevant sources.
    -   Provide concise summaries that other sub-agents can directly consume.
    -   If no relevant information is found, return an empty list and indicate it clearly.
    -   Avoid unnecessary commentary; focus on actionable insights.

    Goal: Ensure the output can be directly used by Competitor, Market Size, Persona, and
    Pitch Deck agents for further processing.
    """,
    output_key='research_data',
    tools=[google_search]
)