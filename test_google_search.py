#!/usr/bin/env python3
"""
Test script to verify Google Search integration in the developer news agent.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_google_search():
    """Test the Google Search functionality."""
    try:
        from dev_news_agent.sub_agents.search_results.agent import search_with_google, search_developer_news_google
        
        print("🔍 Testing Google Search Integration")
        print("=" * 50)
        
        # Test 1: Basic Google Search
        print("\n1. Testing basic Google Search...")
        result = await search_with_google("OpenAI API news", max_results=3)
        print(f"✅ Basic search result length: {len(result)} characters")
        print(f"📄 First 200 chars: {result[:200]}...")
        
        # Test 2: Enhanced Developer News Search
        print("\n2. Testing enhanced developer news search...")
        result2 = await search_developer_news_google("GPT-4o")
        print(f"✅ Enhanced search result length: {len(result2)} characters")
        print(f"📄 First 200 chars: {result2[:200]}...")
        
        print("\n✅ Google Search integration test completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

async def main():
    """Main test function."""
    print("🚀 Google Search Integration Test")
    print("=" * 50)
    
    success = await test_google_search()
    
    if success:
        print("\n🎉 All tests passed! Google Search integration is working.")
        print("\n💡 Benefits of the new integration:")
        print("- ⚡ Much faster than browser automation")
        print("- 🔒 More reliable (no website structure dependencies)")
        print("- 📊 Better search results with Google's algorithms")
        print("- 🎯 Developer-focused filtering")
        print("- 📱 Lower resource usage")
    else:
        print("\n❌ Tests failed. Please check the setup.")

if __name__ == "__main__":
    asyncio.run(main()) 