import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from tools import search_web, save_report
from prompts import AGENT_SYSTEM_PROMPT

load_dotenv()

def create_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0.3
    )

    tools = [search_web, save_report]

    agent = create_react_agent(llm, tools)

    return agent

def run_agent(topic: str):
    print(f"\nResearching: {topic}\n")
    print("=" * 50)

    agent = create_agent()

    result = agent.invoke({
        "messages": [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Research this topic thoroughly: {topic}"}
        ]
    })

    print("\n" + "=" * 50)
    print("FINAL REPORT:")
    final = result["messages"][-1].content
    if isinstance(final, list):
        for block in final:
            if isinstance(block, dict) and block.get("type") == "text":
                print(block["text"])
    else:
        print(final)

if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    run_agent(topic)