import anthropic
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Define tools your agent can use
tools = [
    {
        "name": "calculator",
        "description": "Performs basic math calculations",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate, e.g. '2 + 2'"
                }
            },
            "required": ["expression"]
        }
    }
]

def use_tool(tool_name, tool_input):
    """Execute a tool and return the result."""
    if tool_name == "calculator":
        result = eval(tool_input["expression"])
        return str(result)

def run_agent(user_message):
    """Run the AI agent loop."""
    print(f"\n👤 You: {user_message}")
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        # If Claude is done, print final answer
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"\n🤖 Agent: {block.text}")
            break

        # If Claude wants to use a tool
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    print(f"\n🔧 Using tool: {block.name} with {block.input}")
                    result = use_tool(block.name, block.input)
                    print(f"   Result: {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})

# Run your agent!
run_agent("What is 1234 multiplied by 5678?")