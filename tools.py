from langchain.tools import tool
from duckduckgo_search import DDGS
from datetime import datetime
from ddgs import DDGS

@tool
def search_web(query: str) -> str:
    """Search the web for information about a topic. Input should be a specific search query."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if not results:
                return "No results found for this query."
            
            formatted = []
            for r in results:
                formatted.append(f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}\n")
            
            return "\n---\n".join(formatted)
    except Exception as e:
        return f"Search failed: {str(e)}"

@tool
def save_report(content: str) -> str:
    """Save a research report to a file. Input should be the full report content."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.txt"
        
        with open(filename, "w") as f:
            f.write(content)
        
        return f"Report saved to {filename}"
    except Exception as e:
        return f"Failed to save report: {str(e)}"