from dotenv import load_dotenv
import os
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.tools import RequestsGetTool


from tools import search_tool, wiki_tool, save_tool, fetch_html_tool

load_dotenv()

# OpenRouter LLM setup
openrouter_llm = ChatOpenAI(
    model="openai/gpt-4.1:online",  # Use OpenRouter's web-enabled model
    temperature=0,
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
)

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert web data extraction agent. Your job is to search the HTML content of rental property websites and extract all available rental properties.
            For each property, extract the address, price, and description if available.
            Return your answer strictly as a JSON list of objects, where each object contains 'address', 'price', and 'description' fields. Do not include any other text or formatting.
            Use the available tools to fetch and analyze website HTML as needed.
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool, fetch_html_tool]
agent = create_tool_calling_agent(
    llm=openrouter_llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def extract_rentals_from_website(url: str) -> dict:
    query = f"Extract all available rental properties from {url}. Return a JSON list of objects with address, price, and description."
    raw_response = agent_executor.invoke({"query": query})
    try:
        import json
        output = raw_response.get("output")
        if isinstance(output, str):
            return json.loads(output)
        elif isinstance(output, list) and isinstance(output[0], str):
            return json.loads(output[0])
        elif isinstance(output, list) and isinstance(output[0], dict) and "text" in output[0]:
            return json.loads(output[0]["text"])
        else:
            return {"error": "Unexpected output format", "raw": output}
    except Exception as e:
        return {"error": str(e), "raw_response": raw_response}

if __name__ == "__main__":
    query = input("What can I help you research? ")
    raw_response = agent_executor.invoke({"query": query})
    try:
        structured_response = parser.parse(raw_response.get("output")[0]["text"])
        print(structured_response)
    except Exception as e:
        print("Error parsing response", e, "Raw Response - ", raw_response)