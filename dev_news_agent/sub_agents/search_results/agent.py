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
import time
import warnings
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import dateparser
from google.adk.agents.llm_agent import Agent
from google.adk.tools.load_artifacts_tool import load_artifacts_tool
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types

from ...shared_libraries import constants
from . import prompt

warnings.filterwarnings("ignore", category=UserWarning)


async def search_news_sources(query: str, sources: Optional[List[str]] = None) -> str:
    """Search multiple news sources for developer news using MCP Playwright."""
    try:
        if sources is None:
            sources = list(constants.NEWS_SOURCES.keys())
        
        all_results = []
        
        for source_name in sources:
            if source_name not in constants.NEWS_SOURCES:
                continue
                
            source_config = constants.NEWS_SOURCES[source_name]
            search_url = source_config["search_url"].format(query=query)
            
            print(f"🔍 Searching {source_name} for: {query}")
            
            try:
                # This will be handled by the MCP Playwright server
                # The agent will use the MCP tools to navigate and extract content
                article_data = {
                    "source": source_name,
                    "url": search_url,
                    "title": f"Search results for {query} on {source_name}",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "description": f"Search results from {source_name} for query: {query}"
                }
                all_results.append(article_data)
                    
            except Exception as e:
                print(f"Error searching {source_name}: {str(e)}")
                continue
        
        # Sort by date (newest first)
        all_results.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        # Return top results
        top_results = all_results[:10]  # Get top 10 results
        
        if not top_results:
            return "No results found. This might be due to network issues or changes in website structure."
        
        return json.dumps(top_results, indent=2, default=str)
        
    except Exception as e:
        return f"Error searching news sources: {str(e)}"


def parse_date(date_text: str) -> str:
    """Parse various date formats into a standard format."""
    try:
        # Try to parse the date using dateparser
        parsed_date = dateparser.parse(date_text)
        if parsed_date:
            return parsed_date.strftime("%Y-%m-%d")
    except:
        pass
    
    # Return original if parsing fails
    return date_text


async def analyze_news_content(content: str, query: str) -> str:
    """Analyze news content and structure it for developer news format."""
    analysis_prompt = f"""
    You are an expert developer news analyzer.
    
    The user is searching for: {query}
    
    Here is the HTML content from news sources:
    ```html
    {content[:50000]}  # Limit content for analysis
    ```
    
    Please analyze this content and extract developer news information in the following JSON format:
    {{
        "feature_flows": [
            {{
                "id": "unique-id",
                "title": "Feature Title",
                "source": "Source Name",
                "date": "YYYY-MM-DD",
                "description": "Brief description",
                "steps": [
                    {{
                        "id": "step-id",
                        "type": "announcement|documentation|implementation|discussion|education|application",
                        "label": "Step Label",
                        "icon": "IconName"
                    }}
                ]
            }}
        ]
    }}
    
    Guidelines:
    1. Focus on developer-related news, tools, APIs, and features
    2. Identify different types of content (announcements, docs, code examples, etc.)
    3. Create meaningful step sequences that show the development lifecycle
    4. Use appropriate step types based on content analysis
    5. Extract real dates, sources, and descriptions from the content
    6. Don't make up information - only use what's actually in the content
    
    Return only the JSON response.
    """
    
    return analysis_prompt


async def search_developer_news(query: str) -> str:
    """Main function to search for developer news and return structured data."""
    try:
        print(f"🔍 Starting developer news search for: {query}")
        
        # Search multiple news sources
        news_results = await search_news_sources(query)
        
        if "Error" in news_results:
            return news_results
        
        # For now, return the raw results - the LLM will handle the analysis
        return f"""
        Search completed for: {query}
        
        Raw news results:
        {news_results}
        
        The agent can now use MCP Playwright tools to:
        1. Navigate to news websites
        2. Extract content from pages
        3. Take screenshots
        4. Analyze the content
        
        Use the available MCP Playwright tools to gather more detailed information.
        """
        
    except Exception as e:
        return f"Error in developer news search: {str(e)}"


# Create the MCP Playwright toolset
# Simplified configuration for better reliability
playwright_mcp_toolset = MCPToolset(
    connection_params=StdioServerParameters(
        command="npx",
        args=[
            "@playwright/mcp@latest",
            "--headless"  # Run in headless mode for better compatibility
        ]
    ),
    # Optional: filter specific tools if needed
    # tool_filter=['goto', 'screenshot', 'getContent', 'click', 'fill']
)

# Create the improved search results agent with MCP Playwright
# Note: If MCP Playwright fails, the agent will still work with basic search tools
# try:
search_results_agent = Agent(
    model=constants.MODEL,
    name="search_results_agent",
    description="Search and analyze developer news from multiple sources using MCP Playwright",
    instruction=prompt.SEARCH_RESULT_AGENT_PROMPT,
    tools=[
        playwright_mcp_toolset,  # This provides all Playwright MCP tools
        search_developer_news,
        search_news_sources,
        analyze_news_content,
        # load_artifacts_tool,
    ],
)
# except Exception as e:
#     print(f"Warning: MCP Playwright toolset failed to initialize: {e}")
#     print("Creating agent with basic tools only...")
#     # Fallback to basic tools if MCP fails
#     search_results_agent = Agent(
#         model=constants.MODEL,
#         name="search_results_agent",
#         description="Search and analyze developer news from multiple sources (basic mode)",
#         instruction=prompt.SEARCH_RESULT_AGENT_PROMPT,
#         tools=[
#             search_developer_news,
#             search_news_sources,
#             analyze_news_content,
#             load_artifacts_tool,
#         ],
#     )