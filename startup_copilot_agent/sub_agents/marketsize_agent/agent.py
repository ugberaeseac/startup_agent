from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool
from google.adk.code_executors import BuiltInCodeExecutor

#from startup_copilot_agent.sub_agents.calculator_agent.agent import calculator_agent



retry_config  = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)


marketsize_agent = LlmAgent(
    name='marketsize_agent',
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=retry_config
    ),
    description=
    """
    Market Size Agent for Startup Copilot. Estimates the potential market for a startup idea,
    including total, serviceable, and obtainable markets, to help founders evaluate
    business opportunity size.
    """,
    instruction=
    """
    You are the Market Size Agent. Your task is to estimate market size metrics for a startup idea.

    Output Requirements:

    Return structured JSON with fields:

    -   TAM → Total Addressable Market
    -   SAM → Serviceable Available Market
    -   SOM → Serviceable Obtainable Market
    -   Include data sources if available

    Provide concise, realistic, and actionable estimates
    """,
    output_key='marketsize_data',
    #tools=[AgentTool(calculator_agent)]
)