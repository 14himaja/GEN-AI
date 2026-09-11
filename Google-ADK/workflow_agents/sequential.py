from google.adk.agents import Agent
from google.adk.agents import SequentialAgent


resume_agent = Agent(
    model="gemini-2.0-flash",
    name="resume_agent",
    instruction="Analyze the resume."
)


jd_agent = Agent(
    model="gemini-2.0-flash",
    name="jd_agent",
    instruction="Analyze the job description."
)


matcher_agent = Agent(
    model="gemini-2.0-flash",
    name="matcher_agent",
    instruction="Compare the resume and job description."
)


root_agent = SequentialAgent(
    name="resume_matching_workflow",
    sub_agents=[
        resume_agent,
        jd_agent,
        matcher_agent
    ]
)