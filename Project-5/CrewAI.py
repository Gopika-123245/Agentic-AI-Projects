import os
from crewai import Agent, Task, Crew, Process, LLM

# ==========================================
# GOOGLE API KEY
# ==========================================

os.environ["GOOGLE_API_KEY"] = ""

# ==========================================
# GEMINI MODEL
# ==========================================

llm = LLM(
    model="google/gemini-2.5-flash",
    temperature=0.4
)

# ==========================================
# USER INPUT
# ==========================================

event_name = "College Tech Fest"
budget = "$3000"
guests = 200

# ==========================================
# AGENT 1 — EVENT PLANNER
# ==========================================

planner_agent = Agent(
    role="Event Planner",
    goal="Create an event plan",
    backstory="Expert event organizer.",
    verbose=True,
    llm=llm
)

# ==========================================
# AGENT 2 — BUDGET MANAGER
# ==========================================

budget_agent = Agent(
    role="Budget Manager",
    goal="Optimize event budget",
    backstory="Expert in budget planning.",
    verbose=True,
    llm=llm
)

# ==========================================
# AGENT 3 — RISK ANALYZER
# ==========================================

risk_agent = Agent(
    role="Risk Analyzer",
    goal="Find possible event problems",
    backstory="Expert in risk management.",
    verbose=True,
    llm=llm
)

# ==========================================
# TASK 1
# ==========================================

planning_task = Task(
    description=f"""
    Plan event:
    {event_name}

    Guests: {guests}

    Give:
    - Theme
    - Venue
    - Food
    """,

    expected_output="Simple event plan.",
    agent=planner_agent
)

# ==========================================
# TASK 2
# ==========================================

budget_task = Task(
    description=f"""
    Budget: {budget}

    Check if budget is enough.

    Suggest cheaper options if needed.
    """,

    expected_output="Budget breakdown and savings.",
    agent=budget_agent
)

# ==========================================
# TASK 3
# ==========================================

risk_task = Task(
    description="""
    Analyze event risks.

    Find:
    - Weather issues
    - Crowd problems
    - Food shortages

    Give solutions.
    """,

    expected_output="Risk analysis with solutions.",
    agent=risk_agent
)

# ==========================================
# CREW PIPELINE
# ==========================================

crew = Crew(
    agents=[
        planner_agent,
        budget_agent,
        risk_agent
    ],

    tasks=[
        planning_task,
        budget_task,
        risk_task
    ],

    process=Process.sequential,
    verbose=True
)

# ==========================================
# RUN PIPELINE
# ==========================================

print("\n🚀 Starting AI Event Automation Pipeline...\n")

result = crew.kickoff()

print("\n===================================")
print("🎉 FINAL EVENT REPORT")
print("===================================\n")

print(result)
