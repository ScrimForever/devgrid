import asyncio
from agent.agent_sqs import loop_message


async def main():
    await loop_message()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())