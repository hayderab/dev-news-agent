from google.adk.agents import LlmAgent
from dev_news_agent.tools.rss_feed import get_news_from_rss
from dev_news_agent.tools.google_search import google_search

def create_news_fetcher_agent(model: str, output_key: str) -> LlmAgent:
    return LlmAgent(
        name="NewsFetcher",
        model=model,
        instruction="""You are a news fetcher. You will be provided with a list of keywords in the session state with key 'keywords'.
        You should fetch the news from the internet using the provided tools.
        You should output a JSON object with the tool to call and its parameters. 
        
        Available tools:
        - get_news_from_rss(keywords: list[str]): Fetches news from RSS feeds based on a list of keywords.
        - google_search(query: str): Performs a Google search.

        To use a tool, you must respond with a JSON object in the following format:
        {
            "tool_name": "<the name of the tool to call>",
            "parameters": {
                "<parameter_name>": "<parameter_value>"
            }
        }
        """,
        output_key=output_key
    )
        
