from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Category(str, Enum):
    BUG = "bug"
    FEATURE_REQUEST = "feature_request"
    ACCOUNT_ISSUE = "account_issue"
    BILLING = "billing"
    SUPPORT = "support"
    SPAM = "spam"

class Email(BaseModel):
    id: str
    subject: str
    body: str
    sender: str
    timestamp: str
    priority: Priority
    category: Category

class Action(BaseModel):
    type: str = Field(..., description="Action type")
    email_id: Optional[str] = Field(None, description="Target email ID")
    priority: Optional[Priority] = None
    category: Optional[Category] = None
    response: Optional[str] = None
    next_email: Optional[bool] = Field(False, description="Move to next email")

class Observation(BaseModel):
    current_email: Optional[Email] = None
    inbox: List[Email] = []
    processed_emails: List[Dict[str, Any]] = []
    stats: Dict[str, int] = {}
    message: str = ""
    truncated: bool = False

class Info(BaseModel):
    task_id: str
    step_count: int
    max_steps: int