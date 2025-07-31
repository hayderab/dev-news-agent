
import json
from google.adk.agents import LlmAgent, BaseAgent, LoopAgent, ParallelAgent
from typing import AsyncGenerator
from typing_extensions import override
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
import logging
from pydantic import BaseModel, Field
from typing import List
import re

logger = logging.getLogger(__name__)

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

def sanitize_agent_name(name: str) -> str:
    """Sanitize agent name to be a valid identifier."""
    # Replace spaces and special characters with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Remove multiple consecutive underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    # Ensure it starts with a letter or underscore
    if sanitized and not sanitized[0].isalpha() and sanitized[0] != '_':
        sanitized = f"agent_{sanitized}"
    return sanitized

class NewsOrchestratorAgent(BaseAgent):
    """
    Custom agent for a news generation and orchestration workflow.

    This agent orchestrates a sequence of LLM agents to generate keywords,
    then searches for developer news in parallel for each keyword,
    and aggregates the results.
    """

    # --- Field Declarations for Pydantic ---
    # Declare the agents passed during initialization as class attributes with type hints
    keyword_selector: LlmAgent
    search_results_agent: LlmAgent

    # model_config allows setting Pydantic configurations if needed, e.g., arbitrary_types_allowed
    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        keyword_selector: LlmAgent,
        search_results_agent: LlmAgent,
    ):
        """
        Initializes the NewsOrchestratorAgent.

        Args:
            name: The name of the agent.
            keyword_selector: An LlmAgent to generate the keywords.
            search_results_agent: An LlmAgent template to search and analyze news.
        """
        # Define the sub_agents list for the framework
        sub_agents_list = [
            keyword_selector,
            search_results_agent,
        ]

        # Pydantic will validate and assign them based on the class annotations.
        super().__init__(
            name=name,
            keyword_selector=keyword_selector,
            search_results_agent=search_results_agent,
            sub_agents=sub_agents_list, # Pass the sub_agents list directly
        )

    @override
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        logger.info(f"[{self.name}] Starting news generation workflow.")

        # Step 1: Generate Keywords
        logger.info(f"[{self.name}] Running KeywordSelector...")
        async for event in self.keyword_selector.run_async(ctx):
            yield event

        keywords_data = ctx.session.state.get("keywords")
        if not keywords_data:
            logger.error(f"[{self.name}] No keywords generated. Aborting.")
            return

        # Handle structured output - extract keywords from the Pydantic model
        keywords = []
        if isinstance(keywords_data, dict) and "keywords" in keywords_data:
            # Structured output from Pydantic model
            keywords = keywords_data["keywords"]
        elif isinstance(keywords_data, str):
            # Try to parse as JSON
            try:
                parsed = json.loads(keywords_data)
                if isinstance(parsed, dict) and "keywords" in parsed:
                    keywords = parsed["keywords"]
                elif isinstance(parsed, list):
                    keywords = parsed
                else:
                    keywords = [keywords_data]
            except json.JSONDecodeError:
                # If parsing fails, treat as single keyword
                keywords = [keywords_data]
        elif isinstance(keywords_data, list):
            keywords = keywords_data
        else:
            keywords = [str(keywords_data)]

        # Ensure keywords is a list of strings
        keywords = [str(kw).strip() for kw in keywords if kw and str(kw).strip()]

        if not keywords:
            logger.error(f"[{self.name}] No valid keywords extracted. Aborting.")
            return

        logger.info(f"[{self.name}] Keywords generated: {keywords}")

        # Step 2: Create ParallelAgent dynamically (following StoryFlowAgent pattern)
        logger.info(f"[{self.name}] Creating parallel search agents for all keywords...")

        keyword_agents = []
        for kw in keywords:
            # Sanitize the keyword for use in agent name and output key
            sanitized_kw = sanitize_agent_name(kw)

            # Create specialized agent for this keyword (like StoryFlowAgent creates specialized agents)
            # Replace the placeholder with the actual keyword in the instruction
            instruction_with_keyword = self.search_results_agent.instruction.replace("{search_keyword}", kw)
            keyword_agent = LlmAgent(
                name=f"SearchAgent_{sanitized_kw}",
                model=self.search_results_agent.model,
                instruction=instruction_with_keyword,
                tools=self.search_results_agent.tools,
                output_key=f"search_result_{sanitized_kw}"
            )
            keyword_agents.append(keyword_agent)

        # Create ParallelAgent (exactly like StoryFlowAgent creates LoopAgent and SequentialAgent)
        parallel_search = ParallelAgent(
            name="ParallelKeywordSearch",
            sub_agents=keyword_agents
        )

        # Step 3: Run ParallelAgent (just like StoryFlowAgent runs its workflow agents)
        logger.info(f"[{self.name}] Running ParallelAgent for all {len(keywords)} keywords...")
        async for event in parallel_search.run_async(ctx):
            yield event

        # Step 4: Collect all search results
        fetched_news = {}
        for k in keywords:
            sanitized_k = sanitize_agent_name(k)
            result = ctx.session.state.get(f"search_result_{sanitized_k}")
            if result:
                fetched_news[k] = result

        ctx.session.state["fetched_news"] = fetched_news
        logger.info(f"[{self.name}] All fetched news: {json.dumps(fetched_news, indent=2)}")

        logger.info(f"[{self.name}] News orchestration workflow finished.")