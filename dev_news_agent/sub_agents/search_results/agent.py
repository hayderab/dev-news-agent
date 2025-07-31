# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import json
import os
import time
import warnings
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from google.adk.tools import google_search

import dateparser
from google.adk.agents.llm_agent import Agent
from google.adk.tools.load_artifacts_tool import load_artifacts_tool
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams, StdioServerParameters
from google.genai import types

from ...shared_libraries import constants
from . import prompt

warnings.filterwarnings("ignore", category=UserWarning)


def get_npx_command():
    """Get the appropriate npx command for the current system."""
    # Try common Windows paths first
    windows_paths = [
        "C:\\Program Files\\nodejs\\npx.cmd",
        "C:\\Program Files (x86)\\nodejs\\npx.cmd",
        "npx.cmd",
        "npx"
    ]
    
    # Try common Unix paths
    unix_paths = ["npx", "/usr/bin/npx", "/usr/local/bin/npx"]
    
    # Check Windows paths first
    for path in windows_paths:
        if os.path.exists(path):
            return path
    
    # Fallback to just "npx" and let the system find it
    return "npx"


# Create the MCP Playwright toolset with improved configuration
# def create_playwright_toolset():
#     """Create Playwright MCP toolset with proper error handling."""
#     try:
#         npx_command = get_npx_command()
#         print(f"🔧 Using npx command: {npx_command}")
        
#         playwright_mcp_toolset = MCPToolset(
#             connection_params=StdioConnectionParams(
#                 server_params={
#                     "command": npx_command,
#                     "args": [
#                         "@playwright/mcp@latest",
#                         "--headless"  # Run in headless mode for better compatibility
#                     ]
#                 }
#             ),
#             # Optional: filter specific tools if needed
#             # tool_filter=['goto', 'screenshot', 'getContent', 'click', 'fill']
#         )
#         return playwright_mcp_toolset
#     except Exception as e:
#         print(f"⚠️ Failed to create Playwright MCP toolset: {str(e)}")
#         return None


## sometime npx version does not for , there  is either bug in playwright or google adk , gives subtask error, in that scenario we can use docker
playwright_mcp_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command='docker',
        args=["run", "-i", "--rm", "--init", "--pull=always", "mcr.microsoft.com/playwright/mcp:latest"],
    ),
)

# Create the search results agent with fallback tools only


search_results_agent = Agent(
    model=constants.MODEL,
    name="search_results_agent",
    description="Search and analyze developer news from multiple sources using fallback tools (Playwright MCP temporarily disabled)",
    instruction="use google search to find the latest news about the keyword {search_keyword}, do not worry about contenxt or use information from  ctx.text",
    tools=[
        google_search
        # create_playwright_toolset(),
        # playwright_mcp_toolset,

    ],
)
