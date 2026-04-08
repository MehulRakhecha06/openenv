from fastapi import FastAPI
from models import Observation, Action, Reward, Ticket
import uvicorn

app = FastAPI()

class SupportEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.tickets = {
            "T1": Ticket(id="T1", subject="Login Fail", body="Cannot login to dashboard", customer_tier="enterprise"),
            "T2": Ticket(id="T2", subject="Billing", body="Charged twice this month", customer_tier="basic"),
            "T3": Ticket(id="T3", subject="Slow Load", body="Pages take 10s to load", customer_tier="enterprise")
        }
        self.steps = 10
        return self.state()

    def state(self):
        return Observation(
            current_tickets=list(self.tickets.values()), 
            remaining_steps=self.steps,
            last_action_status="Ready"
        )

    def step(self, action: Action):
        self.steps -= 1
        reward_val = 0.0
        msg = "Action processed"
        
        if action.ticket_id in self.tickets:
            ticket = self.tickets[action.ticket_id]
            if action.action_type == "classify" and action.category:
                ticket.category = action.category
                reward_val += 0.2
            if action.action_type == "prioritize" and action.priority:
                ticket.priority = action.priority
                if ticket.customer_tier == "enterprise" and action.priority == 4:
                    reward_val += 0.3
            if action.action_type == "resolve" and action.resolution_summary:
                ticket.resolution_summary = action.resolution_summary
                reward_val += 0.5
        
        done = self.steps <= 0
        return self.state(), Reward(value=min(reward_val, 1.0), comment=msg), done, {}

# Initialize the environment after the class definition
env = SupportEnv()

@app.get("/")
def read_root():
    """Fixes the 'Not Found' error on the homepage"""
    return {
        "status": "Online",
        "environment": "Support Triage Simulator",
        "location": "server/app.py",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "reset": "/reset (POST)",
            "step": "/step (POST)"
        }
    }

@app.post("/reset")
def reset(): return env.reset()

@app.post("/step")
def step(action: Action): return env.step(action)

@app.get("/state")
def state(): return env.state()

@app.get("/health")
def health(): return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)