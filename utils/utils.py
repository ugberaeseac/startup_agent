from google.genai import types


async def get_agent_response(event):
    if event.content and event.content.parts:
        if (
            event.content.parts[0].text != 'None'
            and event.content.parts[0].text
            ):
            print(event.content.parts[0].text.strip())



async def call_agent_async(runner, user_id, session_id, user_input):
    content = types.Content(
        role='user',
        parts=[types.Part(
            text=user_input
        )]
    )

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            response = await get_agent_response(event)
        return response
    except Exception as e:
        print(f'Error during agent call {e}')
