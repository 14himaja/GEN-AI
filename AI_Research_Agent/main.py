# ==============================
# 1. Imports
# ==============================

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from langchain.agents import create_agent
from datetime import datetime
from simpleeval import simple_eval


# ==============================
# 2. Load Environment Variables
# ==============================

load_dotenv()


# ==============================
# 3. Initialize Gemini
# ==============================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# ==============================
# 4. Create Search Tool
# ==============================

search_tool = DuckDuckGoSearchRun()


# ==============================
# 5. Create Calculator Tool
# ==============================

@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    return str(simple_eval(expression))

# ==============================
# 6. Create Calendar Tool
# ==============================

@tool
def calendar() -> str:
    """Get the current date, day, and time."""
    now = datetime.now()

    return (
        f"Date: {now.strftime('%d %B %Y')}\n"
        f"Day: {now.strftime('%A')}\n"
        f"Time: {now.strftime('%I:%M %p')}"
    )


# ==============================
# 6. Add Tools
# ==============================

tools = [search_tool,calculator,calendar
]


# ==============================
# 7. Create AI Agent
# ==============================

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are an AI Research Assistant.

Use the search tool when the user asks for current or factual information
that may require web research.

Use the calculator tool when mathematical calculations are required.

Use the calendar tool when the user asks for the current date or time.
Give clear and concise answers based on the information you obtain.
"""
)

# ==============================
# 8. Run Agent
# ==============================

question = input("Ask me anything: ")

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": question
        }
    ]
})


# ==============================
# 9. Print Final Answer
# ==============================

print(result["messages"][-1].content)

