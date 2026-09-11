from google.adk.agents import Agent


resume_agent = Agent(
    model="gemini-2.0-flash",
    name="resume_agent",
    description="Handles resume analysis and improvement.",
    instruction="""
    You specialize in resume analysis.

    Analyze resumes, identify weaknesses,
    and suggest improvements.
    """
)


job_agent = Agent(
    model="gemini-2.0-flash",
    name="job_agent",
    description="Handles job description analysis.",
    instruction="""
    You specialize in job description analysis.

    Identify required skills, qualifications,
    and responsibilities.
    """
)


root_agent = Agent(
    model="gemini-2.0-flash",
    name="career_agent",
    description="Coordinates career-related requests.",
    instruction="""
    You are the main career assistant.

    Delegate resume-related requests to resume_agent.
    Delegate job-description-related requests to job_agent.

    Choose the specialist that best matches
    the user's request.
    """,

    sub_agents=[
        resume_agent,
        job_agent
    ]
)