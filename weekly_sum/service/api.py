from fastapi import FastAPI
from ai_agents.weekly_summary_agent import WeeklySummaryAgent
from ai_agents.effort_estimator_agent import estimate_effort_agent

app = FastAPI()

weekly_agent = WeeklySummaryAgent()

@app.get("/")
def root():
    return {"status": "AIRA AI API running"}

@app.post("/weekly-summary")
def weekly_summary(request: dict):
    return weekly_agent.generate_summary(request)

@app.post("/estimate-effort")
def estimate_effort(request: dict):
    return {"effort": estimate_effort_agent(request)}
