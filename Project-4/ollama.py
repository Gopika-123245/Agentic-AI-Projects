from agno.agent import Agent
from agno.models.ollama import Ollama

model = Ollama("llama3.2:1b")

agent = Agent(
    name="Diet Plan",
    model=model,
    instructions="""
You are a Personal diet coach.

Rules:
1. help me to make diet plan
2. whenever you see diet then only respond
otherwise say: please say: it's not a diet plan.
"""
)

print("🐍 Python Interview Agent")
print("Type 'exit' to quit")
print("=" * 50)

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        print("Goodbye 👋")
        break

    response = agent.run(user_input)

    print("\n🤖 Agent:")
    print(response.content)
    print("=" * 50)
