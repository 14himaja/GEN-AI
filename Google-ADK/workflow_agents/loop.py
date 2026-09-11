from google.adk.agents import Agent, LoopAgent


writer_agent = Agent(
    model="gemini-2.0-flash",
    name="writer_agent",
    instruction="Write a draft for the requested topic."
)


reviewer_agent = Agent(
    model="gemini-2.0-flash",
    name="reviewer_agent",
    instruction="Review the draft and identify improvements."
)


root_agent = LoopAgent(
    name="writing_loop",
    sub_agents=[
        writer_agent,
        reviewer_agent
    ],
    max_iterations=3
)