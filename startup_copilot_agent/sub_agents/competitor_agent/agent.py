from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.code_executors import BuiltInCodeExecutor



retry_config  = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)


competitor_agent = LlmAgent(
    name='competitor_agent',
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=retry_config
    ),
    description=
    """
    Competitor Agent for Startup Copilot. Generates a structured competitor map for a startup idea,
    including direct and indirect competitors, strengths, weaknesses, and market positioning,
    based on research data.
    """,
    instruction=
    """
    You are the Competitor Agent. Your task is to analyze competitors for a startup idea using
    Research Agent data: {research_data}.

    -   Output Requirements:
    -   Return structured JSON with fields:
    -   competitor_name
    -   description
    -   strengths
    -   weaknesses
    -   market_position

    Include at least 3-5 key competitors if available
    Focus on concise, actionable insights for startup strategy
    """,
    output_key='competitor_analysis'
)