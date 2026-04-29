from agent.agent import create_agent, run_agent

def main():
    print("=" * 50)
    print("  Academic Research Agent")
    print("  Type 'exit' to quit")
    print("=" * 50)

    agent_executor = create_agent()

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        print("\nAgent: Thinking...\n")
        response = run_agent(agent_executor, user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()