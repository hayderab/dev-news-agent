#!/usr/bin/env python3
"""
Simple test to verify Google Search tool import and basic functionality.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_google_search_import():
    """Test if Google Search tool can be imported and used."""
    try:
        print("🔍 Testing Google Search tool import...")
        
        # Test 1: Import the tool
        from google.adk.tools import google_search
        print("✅ Successfully imported google_search from google.adk.tools")
        
        # Test 2: Try a simple search
        print("🔍 Testing basic Google Search...")
        result = await google_search("OpenAI API news", max_results=3)
        
        if result:
            print(f"✅ Google Search returned {len(result)} results")
            print(f"📄 First result title: {result[0].get('title', 'No title')}")
            return True
        else:
            print("❌ Google Search returned no results")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have the latest google-adk package installed")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

async def test_search_function():
    """Test our search function."""
    try:
        print("\n🔍 Testing our search function...")
        
        from dev_news_agent.sub_agents.search_results.agent import search_with_google
        
        result = await search_with_google("OpenAI API news", max_results=3)
        
        if result and "Error" not in result:
            print(f"✅ Our search function returned results ({len(result)} chars)")
            return True
        else:
            print(f"❌ Our search function failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Function test error: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Google Search Tool Test")
    print("=" * 50)
    
    # Test 1: Import and basic functionality
    import_success = await test_google_search_import()
    
    # Test 2: Our search function
    function_success = await test_search_function()
    
    if import_success and function_success:
        print("\n🎉 All tests passed! Google Search is working correctly.")
        print("\n💡 The agent should now use Google Search for fast, reliable results.")
    else:
        print("\n❌ Some tests failed. Please check the setup.")
        
        if not import_success:
            print("\n🔧 Troubleshooting:")
            print("1. Make sure you have the latest google-adk package:")
            print("   pip install --upgrade google-adk")
            print("2. Check your ADK configuration")
            print("3. Verify API credentials")

if __name__ == "__main__":
    asyncio.run(main()) 