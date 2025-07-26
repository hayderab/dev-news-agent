#!/usr/bin/env python3
"""
Simple test for the simplified search approach.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_simple_search():
    """Test the simplified search approach."""
    try:
        print("🔍 Testing simplified search...")
        
        from dev_news_agent.sub_agents.search_results.agent import search_developer_news_google
        
        # Test with a simple query
        result = await search_developer_news_google("OpenAI")
        
        print(f"✅ Search completed!")
        print(f"📄 Result length: {len(result)} characters")
        print(f"📄 First 300 chars: {result[:300]}...")
        
        if "Error" not in result and "No results" not in result:
            print("✅ Search returned results successfully!")
            return True
        else:
            print(f"❌ Search failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

async def test_agent_tools():
    """Test that the agent has the simplified tool set."""
    try:
        print("\n🔍 Testing agent tool configuration...")
        
        from dev_news_agent.sub_agents.search_results.agent import search_results_agent
        
        print(f"✅ Agent name: {search_results_agent.name}")
        print(f"✅ Number of tools: {len(search_results_agent.tools)}")
        
        # Get tool names
        tool_names = []
        for tool in search_results_agent.tools:
            if hasattr(tool, '__name__'):
                tool_names.append(tool.__name__)
            else:
                tool_names.append(str(type(tool).__name__))
        
        print(f"✅ Tools: {tool_names}")
        
        # Should only have 2 tools now
        if len(tool_names) == 2:
            print("✅ Simplified tool set - perfect!")
            return True
        else:
            print(f"❌ Too many tools: {len(tool_names)}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Simplified Search Test")
    print("=" * 50)
    
    # Test 1: Tool configuration
    tools_success = await test_agent_tools()
    
    # Test 2: Search functionality
    search_success = await test_simple_search()
    
    if tools_success and search_success:
        print("\n🎉 Simplified approach is working!")
        print("\n💡 The agent now has:")
        print("- Only 2 tools (much simpler)")
        print("- Clear, direct prompt")
        print("- Simple Google Search function")
        print("\n🔧 Try asking the agent for 'OpenAI news' now!")
    else:
        print("\n❌ Some issues found.")
        print("\n🔧 Please check:")
        print("1. That all files were saved")
        print("2. That you're using the updated code")
        print("3. That Google Search API is available")

if __name__ == "__main__":
    asyncio.run(main()) 