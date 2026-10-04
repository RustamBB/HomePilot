import asyncio

from homepilot_agent.mcp_client import connect


async def main():
    async with connect() as c:
        print(await c.call("demo_reset"))


asyncio.run(main())
