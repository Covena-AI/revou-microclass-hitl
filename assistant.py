from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from state import State
from tools import create_event, read_events, update_event, delete_event, read_sheet, update_sheet, delete_row
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State):
        while True:
            result = self.runnable.invoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

primary_assistant_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful personal assistant. "
            "Use the provided tools to manage Google Calendar for scheduling meetings "
            "and Google Sheets for personal finance management. "
            "When using these tools, be precise and efficient. "
            "If a task requires multiple steps, break it down and use the appropriate tools for each step."
            "\nFor google sheets, you should grab from column A to E"
            "\nCurrent time: {time}, timezone: {timezone}."
            "\nMy day starts at 8am and ends at 10pm. Schedule meetings accordingly.",
        ),
        ("placeholder", "{messages}"),
    ]
).partial(time=datetime.now(), timezone="America/Los_Angeles")

safe_tools = [
    read_events,
    read_sheet,
]

sensitive_tools = [
    create_event,
    update_event,
    delete_event,
    update_sheet,
    delete_row,
]

sensitive_tool_names = {tool.name for tool in sensitive_tools}

personal_assistant_runnable = primary_assistant_prompt | llm.bind_tools(safe_tools + sensitive_tools)

# Initialize the Assistant
assistant = Assistant(personal_assistant_runnable)
