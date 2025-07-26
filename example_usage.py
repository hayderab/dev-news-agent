#!/usr/bin/env python3
"""
Example usage of the Developer News Agent.

This script demonstrates how to use the agent to search for developer news
and get structured results.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def search_developer_news(query: str):
    """Search for developer news using the agent."""
    try:
        from dev_news_agent.agent import root_agent
        
        print(f"🔍 Searching for: {query}")
        print("=" * 50)
        
        # Run the agent with the search query
        response = await root_agent.run(f"Search for {query} news")
        
        print("\n📰 Search Results:")
        print("=" * 50)
        print(response)
        
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

async def main():
    """Main function to demonstrate agent usage."""
    print("🚀 Developer News Agent Example")
    print("=" * 50)
    
    # Example search queries
    example_queries = [
        "GPT-4o",
        "Claude 3.5",
        "Gemini API",
        "React 19",
        "Next.js 15"
    ]
    
    print("Available example queries:")
    for i, query in enumerate(example_queries, 1):
        print(f"  {i}. {query}")
    
    print("\nEnter a number (1-5) to search, or type your own query:")
    user_input = input("> ").strip()
    
    # Parse user input
    if user_input.isdigit() and 1 <= int(user_input) <= len(example_queries):
        query = example_queries[int(user_input) - 1]
    else:
        query = user_input
    
    if not query:
        print("No query provided. Using default: GPT-4o")
        query = "GPT-4o"
    
    # Perform the search
    result = await search_developer_news(query)
    
    if result:
        print("\n✅ Search completed successfully!")
        print("\n💡 Tips:")
        print("- The agent searches multiple tech news sources")
        print("- Results are structured in JSON format")
        print("- You can customize the search query")
        print("- Set HEADLESS_MODE=false in .env to see the browser in action")
    else:
        print("\n❌ Search failed. Please check your setup.")

if __name__ == "__main__":
    asyncio.run(main()) 