import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from startup_copilot_agent.agent import startup_copilot_agent
from utils.utils import call_agent_async




load_dotenv()


session_service = InMemorySessionService()

#Define initial state
initial_state = {
  "idea": "",
  "outputs": {
    "research": {},
    "competitors": {},
    "market_size": {},
    "personas": {},
    "pricing": {},
    "pitch_deck": {}
  },
  "done": []
}

async def main_async():
    APP_NAME='startup_copilot_agent'
    USER_ID='ugberaeseac'

    #check for existing sessions
    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID
    )

    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f'Continuing existing session: {SESSION_ID}')
    else:
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state
        )
        SESSION_ID = new_session.id
        print(f'Created new session: {SESSION_ID}')

    #create runner
    runner = Runner(
        agent=startup_copilot_agent,
        app_name=APP_NAME,
        session_service=session_service
    )

    print('Welcome to Startup Copilot Agent!')
    print('Type "exit" or "quit" to end the conversation\n')

    while True:
        user_input = input('<You>: ')
        if user_input.lower() in ['exit', 'quit']:
            print('Ending Conversation. Goodbye!')
            break

        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


if __name__ == '__main__':
    asyncio.run(main_async())