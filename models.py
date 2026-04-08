from pydantic import BaseModel
from typing import Optional

class Ticket(BaseModel):
    id: str
    subject: str
    body: str
    customer_tier: str
    # These MUST be defined here to be used in app.py
    category: Optional[str] = None
    priority: Optional[int] = None
    resolution_summary: Optional[str] = None

class Observation(BaseModel):
    current_tickets: List[Ticket]
    remaining_steps: int
    last_action_status: str = "Ready" # Default value prevents the crash

class Action(BaseModel):
    action_type: str = Field(..., description="classify, prioritize, or resolve")
    ticket_id: str
    category: Optional[str] = None
    priority: Optional[int] = None
    resolution_summary: Optional[str] = None

class Reward(BaseModel):
    value: float
    comment: str