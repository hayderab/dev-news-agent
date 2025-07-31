import os
import asyncio
import Basemo
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

# ✅ Set your API key securely
os.environ["GOOGLE_API_KEY"] = "AIzaSyDLA4jrlu_9ehwm1lKc0OjJlT7gQWf7y9M"

# ✅ Full path to the MCP-compatible tool server (e.g. Playwright or math server)
server_params = StdioServerParameters(
    command="npx",  # for Playwright MCP server
    args=["@playwright/mcp@latest"],
    # OR, for a Python MCP server (like math):
    # command="python",
    # args=["/absolute/path/to/math_server.py"],
)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # Load tools exposed by the MCP server
            tools = await load_mcp_tools(session)

            # Build agent using Gemini via LangChain model name
            agent = create_react_agent(llm, tools)

            # Ask a question using standard message format
            response = await agent.ainvoke({
                "messages": [
                    {"role": "user", "content": "What's the latest OpenAI developer news?"}
                ]
            })
            return response

            

# Run the async agent
asyncio.run(main())
