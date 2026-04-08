from typing import List, Optional
from pydantic import BaseModel,Field

class Ticket(BaseModel):
    id: str
    subject: str
    body: str
    customer_tier: str
    category: Optional[str] = None
    priority: Optional[int] = None
    resolution_summary: Optional[str] = None

class Observation(BaseModel):
    current_tickets: List[Ticket]  # This is where the error was!
    remaining_steps: int
    last_action_status: str

class Action(BaseModel):
    action_type: str = Field(..., description="classify, prioritize, or resolve")
    ticket_id: str
    category: Optional[str] = None
    priority: Optional[int] = None
    resolution_summary: Optional[str] = None

class Reward(BaseModel):
    value: float
    comment: str
