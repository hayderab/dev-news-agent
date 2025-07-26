#!/usr/bin/env python3
"""
Test to verify the agent has Google Search tools properly configured.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_agent_tools():
    """Test that the agent has the correct tools configured."""
    try:
        print("🔍 Testing agent tool configuration...")
        
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
        
        # Check for Google Search tools
        google_tools = [name for name in tool_names if 'google' in name.lower()]
        if google_tools:
            print(f"✅ Found Google Search tools: {google_tools}")
        else:
            print("❌ No Google Search tools found!")
            return False
        
        # Check tool order (Google tools should be first)
        first_tools = tool_names[:3]
        print(f"✅ First 3 tools: {first_tools}")
        
        # Check if Google tools are in the first few positions
        if any('google' in name.lower() for name in first_tools):
            print("✅ Google Search tools are prioritized correctly")
            return True
        else:
            print("❌ Google Search tools are not in the first positions")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

async def test_agent_prompt():
    """Test that the agent has the updated prompt."""
    try:
        print("\n🔍 Testing agent prompt...")
        
        from dev_news_agent.sub_agents.search_results.agent import search_results_agent
        
        prompt = search_results_agent.instruction
        
        # Check for Google Search mentions in prompt
        google_mentions = prompt.lower().count('google')
        print(f"✅ Google mentioned {google_mentions} times in prompt")
        
        # Check for specific tool mentions
        if 'search_developer_news_google' in prompt:
            print("✅ Prompt mentions search_developer_news_google")
        else:
            print("❌ Prompt doesn't mention search_developer_news_google")
            return False
        
        if 'search_all_ai_companies_google' in prompt:
            print("✅ Prompt mentions search_all_ai_companies_google")
        else:
            print("❌ Prompt doesn't mention search_all_ai_companies_google")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt test error: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Agent Tool Configuration Test")
    print("=" * 50)
    
    # Test 1: Tool configuration
    tools_success = await test_agent_tools()
    
    # Test 2: Prompt configuration
    prompt_success = await test_agent_prompt()
    
    if tools_success and prompt_success:
        print("\n🎉 Agent is properly configured for Google Search!")
        print("\n💡 The agent should now prioritize Google Search tools.")
        print("\n🔧 If it's still not working, try:")
        print("1. Restart your Python environment")
        print("2. Clear any cached imports")
        print("3. Check if the agent is using the updated code")
    else:
        print("\n❌ Agent configuration issues found.")
        print("\n🔧 Please check:")
        print("1. That all files were saved properly")
        print("2. That you're running the updated agent code")
        print("3. That there are no import errors")

if __name__ == "__main__":
    asyncio.run(main()) 