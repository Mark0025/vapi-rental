from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun, RequestsGetTool
from langchain_community.utilities import WikipediaAPIWrapper, RequestsWrapper
from langchain.tools import Tool
from datetime import datetime

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

fetch_html_tool = Tool(
    name="fetch_html",
    func=RequestsGetTool(
        requests_wrapper=RequestsWrapper(),
        allow_dangerous_requests=True
    ).run,
    description="Fetches the raw HTML content of a web page for further analysis or extraction. Use this to get the actual listings from a rental website."
)