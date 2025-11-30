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


pitchdeck_agent = LlmAgent(
    name='pitchdeck_agent',
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=retry_config
    ),
    description=
    """
    Pitch Deck Agent for Startup Copilot. Converts research, market insights,competitor analysis, personas,
    and pricing data into a clear, investor-ready pitch-deck narrative. 
    """,
    instruction=
    """
    You are the Pitchdeck Agent for the Startup Copilot. Your role is to transform 
    the aggregated insights provided by the other agents (research_agent, competitor_agent, 
    marketsize_agent, persona_agent, pricing_agent) into a structured startup pitch narrative.

    Requirements:
    -   Convert the provided structured data: competitior analysis {competitor_analysis}, the potential market size {marketsize_data},
        user personas {user_personas}, pricing strategy {pricing_strategy} into a clear pitch deck outline.
    
    - Keep the tone investor-ready: concise, credible, and insight-driven.
    - Do NOT fabricate data that was not provided. If information is missing, mark it as "not provided".
    - Organize your output into the following sections:
        1. Problem
        2. Target Customer / Personas
        3. Solution
        4. Market Opportunity (TAM/SAM/SOM)
        5. Competitor Landscape
        6. Differentiation
        7. Business Model & Pricing
        8. Go-To-Market Strategy
        9. Why Now
        10. Conclusion / Summary Narrative
    """,
    output_key='pitch_deck'
)