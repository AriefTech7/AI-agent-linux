from langchain.tools import tool
from .service import WebSearchTool
from typing import Any,Dict
search_tool = WebSearchTool()


@tool
def web_search_basic(query: str) -> Dict[str, Any]:
    """
    Search the web quickly and efficiently.

    Use this tool for simple, factual questions, brief definitions,
    latest news, or information that does not require in-depth analysis.

    Do not use this tool for complex research, multi-source comparisons,
    or technical questions requiring further verification.

    Args:
    query: The question or keywords to search for.

    Returns:
    Dict: Search results containing a summary and a list of web sources.
    """

    return search_tool.search_basic(query)


@tool
def web_search_advanced(query: str) -> Dict[str, Any]:
    """
    Search the web with advanced mode for more in-depth research.

    Use this tool for complex questions, technical analysis, comparisons,
    multi-source investigations, or topics that require a higher level of confidence.

    This tool is more powerful than web_search_basic, but may generate
    more context and take longer.

    Args:
    query: The question or keyword you want to search for in depth.

    Returns:
    Dict: Advanced search results containing a summary and a list of web sources.
    """
    return search_tool.search_advanced(query)


# @tool
# def web_search_fast(query: str) -> Dict[str, Any]:
#     """
#     Performs a rapid web search to meet immediate information needs.

#     Use this tool when the user requires quick answers, brief facts,
#     simple validation, news headlines, entity names, short definitions, or
#     information likely to be available directly in the top search results.

#     This mode prioritizes speed and token efficiency, making it unsuitable
#     for in-depth research, complex analysis, multi-source comparisons, or
#     queries requiring further verification.

#     Args:
#     query: The question or keywords for the quick search.

#     Returns:
#     Dict: Quick search results containing top web sources.
#     """

#     return search_tool.search_fast(query)
