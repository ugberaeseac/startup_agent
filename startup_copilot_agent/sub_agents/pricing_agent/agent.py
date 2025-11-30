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


pricing_agent = LlmAgent(
    name='pricing_agent',
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=retry_config
    ),
    description=
    """
    Pricing Agent for Startup Copilot. Suggests monetization strategies and recommended pricing
    for a startup's products or services based on competitors, market data, and target customer
    willingness to pay.
    """,
    instruction=
    """
    You are the Pricing Agent. Your task is to propose a pricing strategy for a startup idea.

    Output Requirements:

    Return structured JSON with fields:
    -   pricing_model (e.g., subscription, freemium, one-time fee)
    -   recommended_price_range
    -   rationale

    Base recommendations on competitor pricing, market trends, and target audience insights
    Ensure output is concise, actionable, and ready for startup planning
    """,
    output_key='pricing_strategy'
)