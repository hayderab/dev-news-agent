from .sub_agents.orchestrator.agent import NewsOrchestratorAgent
from .sub_agents.keyword_selector.agent import create_keyword_selector_agent
from .sub_agents.search_results.agent import search_results_agent
from google.adk.agents.llm_agent import Agent

GEMINI_MODEL = "gemini-2.0-flash"


keyword_selector = create_keyword_selector_agent(
    model=GEMINI_MODEL,
    output_key="keywords",
)

root_agent = NewsOrchestratorAgent(
    name="NewsOrchestratorAgent",
    keyword_selector=keyword_selector,
    search_results_agent=search_results_agent,
)







