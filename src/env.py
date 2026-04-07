"""
Email Triage Environment - Complete OpenEnv Implementation
Real-world customer support email classification task
"""

import random
import json
from typing import Tuple, Dict, Any, Optional, List
from pydantic import ValidationError, Field

# Local imports
from .models import (
    Observation, Action, Info, Email, Priority, Category
)
from .tasks import TASKS, generate_emails
from .grader import EmailTriageGrader


class EmailTriageEnv:
    """
    OpenEnv-compliant email triage environment.
    
    Tasks: Classify customer support emails by priority and category.
    Rewards: Dense signal for partial progress + completion bonus.
    """
    
    def __init__(self, task_id: str = "easy"):
        """Initialize with task difficulty."""
        if task_id not in TASKS:
            raise ValueError(f"Invalid task_id. Choose: {list(TASKS.keys())}")
        
        self.task_id = task_id
        self.task_config = TASKS[task_id]
        self.grader = EmailTriageGrader()
        self.reset()
    
    def reset(self) -> Tuple[Observation, Info]:
        """Reset environment to initial state."""
        # Generate emails for this task
        self.inbox: List[Email] = generate_emails(self.task_id, self.task_config["num_emails"])
        self.processed_emails: List[Dict[str, Any]] = []
        self.current_email_idx: int = 0
        self.step_count: int = 0
        self.max_steps: int = self.task_config["max_steps"]
        
        # Ground truth for grading
        self.true_emails: Dict[str, Dict[str, Any]] = {
            email.id: email.dict() for email in self.inbox
        }
        
        obs = self._build_observation()
        info = Info(
            task_id=self.task_id,
            step_count=self.step_count, 
            max_steps=self.max_steps
        )
        
        return obs, info
    
    def step(self, action_input: Dict[str, Any]) -> Tuple[Observation, float, bool, bool, Info]:
        """
        Take action and return (obs, reward, done, truncated, info).
        
        Accepts dict input for easy LLM parsing.
        """
        self.step_count += 1
        
        # Parse action safely
        try:
            action = Action(**action_input)
        except ValidationError:
            action = Action(type="next")  # Safe default
        
        reward = 0.0
        done = False
        truncated = self.step_count >= self.max_steps
        
        # Process action
        if action.type == "analyze":
            reward += 0.1  # Engagement bonus
            
        elif action.type == "classify":
            reward += self._process_classification(action)
            
        elif action.type == "next":
            self._advance_email()
            reward += 0.05  # Progress bonus
            
        elif action.type == "skip":
            reward += self._process_skip(action)
            
        else:
            reward -= 0.3  # Invalid action penalty
        
        # Check for completion
        if self._is_complete():
            done = True
            completion_score = self.grader.grade_task(
                self.processed_emails, 
                self.true_emails, 
                self.task_config
            )
            reward += completion_score * 2.0  # Big completion bonus
        
        # Efficiency penalty
        if self.step_count > self.max_steps * 0.8:
            reward -= 0.1
        
        # Clamp reward
        reward = max(-1.0, min(3.0, reward))
        
        obs = self._build_observation()
        info = Info(
            task_id=self.task_id,
            step_count=self.step_count,
            max_steps=self.max_steps
        )
        
        return obs, reward, done, truncated, info
    
    def state(self) -> Dict[str, Any]:
        """Return complete environment state for debugging."""
        return {
            "task_id": self.task_id,
            "task_config": self.task_config,
            "inbox": [e.dict() for e in self.inbox],
            "processed_emails": self.processed_emails,
            "current_email_idx": self.current_email_idx,
            "step_count": self.step_count,
            "true_emails": self.true_emails,
            "final_score": self.grader.grade_task(
                self.processed_emails, self.true_emails, self.task_config
            )
        }
    
    def _build_observation(self) -> Observation:
        """Build observation with truncation for LLM context limits."""
        current_email = self.inbox[self.current_email_idx] if self.inbox else None
        
        # Truncate long content
        truncated = False
        if current_email:
            max_len = 800
            full_text = f"{current_email.subject}\n\n{current_email.body}"
            if len(full_text) > max_len:
                current_email.body = full_text[:max_len] + "... [truncated]"
                truncated = True
        
        # Recent activity
        recent_processed = self.processed_emails[-3:] if self.processed_emails else []
        
        stats = {
            "inbox_size": len(self.inbox),
            "processed_count": len(self.processed_emails),
            "current_index": self.current_email_idx,
            "step_count": self.step_count,
            "progress": f"{len(self.processed_emails)}/{len(self.inbox)}"
        }
        
        message = (
            f"Triage Task: {self.task_config['name']} "
            f"({stats['progress']}) | Steps: {self.step_count}/{self.max_steps}"
        )
        
        return Observation(
            current_email=current_email,
            inbox=self.inbox[:3],  # Preview next emails
            processed_emails=recent_processed,
            stats=stats,
            message=message,
            truncated=truncated
        )
    
    def _process_classification(self, action: Action) -> float:
        """Process classification action and return reward."""
        if not action.email_id or not action.priority or not action.category:
            return -0.2  # Incomplete classification
        
        target_email = next((e for e in self.inbox if e.id == action.email_id), None)
        if not target_email:
            return -0.3  # Invalid email ID
        
        # Record classification
        self.processed_emails.append({
            "email_id": action.email_id,
            "priority": action.priority,
            "category": action.category,
            "completed": True,
            "step": self.step_count
        })
        
        # Calculate accuracy-based reward
        true_priority = target_email.priority
        true_category = target_email.category
        
        priority_correct = 1.0 if action.priority == true_priority else 0.4
        category_correct = 1.0 if action.category == true_category else 0.3
        
        # Advance to next email
        self._advance_email()
        
        return (priority_correct * 0.6) + (category_correct * 0.4)
    
    def _process_skip(self, action: Action) -> float:
        """Process skip action (with penalty)."""
        if action.email_id:
            self.processed_emails.append({
                "email_id": action.email_id,
                "priority": None,
                "category": None,
                "completed": False,
                "step": self.step_count
            })
            self._advance_email()
        
        return -0.25  # Skip penalty
    
    def _advance_email(self):
        """Move to next unprocessed email."""
        processed_ids = {p["email_id"] for p in self.processed_emails}
        
        # Find next unprocessed email
        for i in range(len(self.inbox)):
            idx = (self.current_email_idx + i + 1) % len(self.inbox)
            if self.inbox[idx].id not in processed_ids:
                self.current_email_idx = idx
                return
        
        # All processed, stay on last
        self.current_email_idx = len(self.inbox) - 1
    
    def _is_complete(self) -> bool:
        """Check if task is complete."""
        return len(self.processed_emails) >= self.task_config["num_emails"]


# OpenEnv compatibility wrapper
def make_env(task_id: str = "easy"):
    """Factory function for OpenEnv."""
    return EmailTriageEnv(task_id)