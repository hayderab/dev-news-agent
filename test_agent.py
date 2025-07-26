#!/usr/bin/env python3
"""
Simple test script to verify the developer news agent setup.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_agent_import():
    """Test that the agent can be imported and initialized."""
    try:
        from dev_news_agent.agent import root_agent
        print("✅ Successfully imported root_agent")
        
        # Test that the agent has the expected attributes
        assert hasattr(root_agent, 'name'), "Agent should have a name"
        assert hasattr(root_agent, 'tools'), "Agent should have tools"
        assert hasattr(root_agent, 'instruction'), "Agent should have instructions"
        
        print(f"✅ Agent name: {root_agent.name}")
        print(f"✅ Number of tools: {len(root_agent.tools)}")
        
        # Handle tools that might not have __name__ attribute
        tool_names = []
        for tool in root_agent.tools:
            if hasattr(tool, '__name__'):
                tool_names.append(tool.__name__)
            else:
                tool_names.append(str(type(tool).__name__))
        print(f"✅ Tools: {tool_names}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_constants():
    """Test that constants are properly configured."""
    try:
        from dev_news_agent.shared_libraries import constants
        
        print(f"✅ Model: {constants.MODEL}")
        print(f"✅ Headless mode: {constants.HEADLESS_MODE}")
        print(f"✅ Browser timeout: {constants.BROWSER_TIMEOUT}")
        print(f"✅ News sources: {list(constants.NEWS_SOURCES.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Constants error: {e}")
        return False

async def main():
    """Run all tests."""
    print("🧪 Testing Developer News Agent Setup")
    print("=" * 50)
    
    # Test imports
    agent_ok = await test_agent_import()
    print()
    
    # Test constants
    constants_ok = await test_constants()
    print()
    
    if agent_ok and constants_ok:
        print("🎉 All tests passed! The agent is ready to use.")
        print("\nNext steps:")
        print("1. Install Node.js and npx: https://nodejs.org/en/")
        print("2. Set up your .env file with API keys")
        print("3. Run the agent: python -c \"from dev_news_agent.agent import root_agent; print('Agent ready!')\"")
    else:
        print("❌ Some tests failed. Please check the setup.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 