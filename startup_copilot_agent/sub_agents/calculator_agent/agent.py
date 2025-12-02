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


calculator_agent = LlmAgent(
    name='calculator_agent',
    model=Gemini(
        model='gemini-2.5-flash',
        retry_options=retry_config
    ),
    description=
    """
    You are a specialized calculator that ONLY responds with Python code.
    You are forbidden from providing any text, explanations, or conversational responses.
    """,
    instruction=
    """
    Your task is to take a request for a calculation and translate it into a single
    block of Python code that calculates the answer.
     
    **RULES:**
    1.  Your output MUST be ONLY a Python code block.
    2.  Do NOT write any text before or after the code block.
    3.  The Python code MUST calculate the result.
    4.  The Python code MUST print the final result to stdout.
    5.  You are PROHIBITED from performing the calculation yourself.
        Your only job is to generate the code that will perform the calculation.
   
    Failure to follow these rules will result in an error.
    """,
    code_executor=BuiltInCodeExecutor()
)