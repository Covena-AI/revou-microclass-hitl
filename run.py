import uuid
from graph import personal_assistant_graph
from util import _print_event
from langchain_core.messages import ToolMessage

# Update with the backup file so we can restart from the original place in each section
thread_id = str(uuid.uuid4())
print("THREAD ID", thread_id)

config = {
    "configurable": {
        # Checkpoints are accessed by thread_id
        "thread_id": thread_id,
    }
}

_printed = set()

print("Welcome to the personal assistant. Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break
    
    events = personal_assistant_graph.stream(
        {"messages": ("user", user_input)}, config, stream_mode="values"
    )
    for event in events:
        _print_event(event, _printed)
    
    snapshot = personal_assistant_graph.get_state(config)
    while snapshot.next:
        # We have an interrupt! The agent is trying to use a tool, and the user can approve or deny it
        try:
            user_approval = input(
                "Do you approve of the above actions? Type 'y' to continue;"
                " otherwise, explain your requested changes.\n\n"
            )
        except:
            user_approval = "y"
        
        if user_approval.strip().lower() == "y":
            # Just continue
            result = personal_assistant_graph.stream(
                None,
                config,
                stream_mode="values"
            )
        else:
            # Satisfy the tool invocation by
            # providing instructions on the requested changes / change of mind
            result = personal_assistant_graph.stream(
                {
                    "messages": [
                        ToolMessage(
                            tool_call_id=event["messages"][-1].tool_calls[0]["id"],
                            content=f"API call denied by user. Reasoning: '{user_approval}'. Continue assisting, accounting for the user's input.",
                        )
                    ]
                },
                config,
                stream_mode="values"
            )
        
        for event in result:
            _print_event(event, _printed)
        
        # Update the snapshot
        snapshot = personal_assistant_graph.get_state(config)
