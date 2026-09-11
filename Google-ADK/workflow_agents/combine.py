from google.adk.agents import Agent
from google.adk.agents import SequentialAgent, ParallelAgent


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


analysis_agents = ParallelAgent(
    name="analysis_agents",
    sub_agents=[
        resume_agent,
        jd_agent
    ]
)


matcher_agent = Agent(
    model="gemini-2.0-flash",
    name="matcher_agent",
    instruction="Compare the resume analysis with the job description analysis."
)


recommendation_agent = Agent(
    model="gemini-2.0-flash",
    name="recommendation_agent",
    instruction="Generate recommendations based on the matching results."
)


root_agent = SequentialAgent(
    name="resume_matching_workflow",
    sub_agents=[
        analysis_agents,
        matcher_agent,
        recommendation_agent
    ]
)