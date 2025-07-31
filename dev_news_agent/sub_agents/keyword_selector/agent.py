from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List

class KeywordsOutput(BaseModel):
    """Structured output for keyword selection."""
    keywords: List[str] = Field(
        description="List of relevant keywords for developer news search",
        min_items=1,
        max_items=10
    )

def create_keyword_selector_agent(model: str, output_key: str) -> LlmAgent:
    return LlmAgent(
        name="KeywordSelector",
        model=model,
        instruction="""You are a keyword selector. From the user query, select the keywords that are relevant to developer news, specifically focusing on platforms like OpenAI, Claude, and Gemini.
        The user will provide the query in the session state with key 'query'.
        You should output the keywords as a list of strings.
        """,
        input_schema=None,
        output_schema=KeywordsOutput,  # Use the Pydantic model
        output_key=output_key,
    )
