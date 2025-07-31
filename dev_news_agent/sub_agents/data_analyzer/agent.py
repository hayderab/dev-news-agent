from google.adk.agents import LlmAgent

def create_data_analyzer_agent(model: str, output_key: str) -> LlmAgent:
    return LlmAgent(
        name="DataAnalyzer",
        model=model,
        instruction="""You are a data analyzer. You will be provided with a list of news in the session state with key 'fetched_news'.
        You should analyze the news and provide a summary of the news.
        You should output the summary as a string.
        """,
        input_schema=None,
        output_key=output_key,
    )
