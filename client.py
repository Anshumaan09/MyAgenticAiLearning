import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

async def main():
    # Construct absolute path to mathserver.py so subprocess can find it
    mathserver_path = os.path.abspath("mathserver.py")

    client = MultiServerMCPClient(
        {
            "math": {
                "command": sys.executable,          # use same .venv python
                "args": [mathserver_path],
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http"      # underscore, not hyphen
            }
        }
    )

    tools = await client.get_tools()
    print("Available tools:", [t.name for t in tools])

    model = ChatGroq(model="llama-3.3-70b-versatile")
    agent = create_react_agent(model, tools)

    math_response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "What is the square root of 16?"}]
    })

    weather_response = await agent.ainvoke({
        "messages": [{"role": "user", "content": "What is the weather in New York?"}]
    })

    print("Math response: ", math_response["messages"][-1].content)
    print("Weather response: ", weather_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
