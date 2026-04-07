import random
from typing import List
from .models import Email, Priority, Category

TASKS = {
    "easy": {
        "task_id": "easy",
        "name": "Easy Triage", 
        "description": "Triage 5 simple emails with obvious keywords",
        "num_emails": 5,
        "max_steps": 25
    },
    "medium": {
        "task_id": "medium",
        "name": "Medium Triage",
        "description": "Triage 8 emails requiring context understanding", 
        "num_emails": 8,
        "max_steps": 50
    },
    "hard": {
        "task_id": "hard",
        "name": "Hard Triage",
        "description": "Triage 12 complex emails with ambiguous language",
        "num_emails": 12, 
        "max_steps": 100
    }
}

# COMPLETE email templates - FIXED KeyError
TEMPLATES = {
    Category.BUG: [
        ("URGENT: App crashing!", "App crashes on login. Error 500. Can't access account.", Priority.URGENT),
        ("Button broken", "Submit button doesn't work after form.", Priority.MEDIUM),
        ("UI glitch", "Dropdown menu overlaps text.", Priority.LOW),
    ],
    Category.FEATURE_REQUEST: [
        ("New feature idea", "Please add dark mode toggle.", Priority.MEDIUM),
        ("Integration request", "Need Zapier integration for workflows.", Priority.LOW),
    ],
    Category.ACCOUNT_ISSUE: [
        ("Can't login", "Password reset not working. Account locked.", Priority.HIGH),
        ("Username taken?", "Is john.doe.2024 available?", Priority.LOW),
    ],
    Category.BILLING: [
        ("Wrong charge!", "Charged $99 but basic plan is $9.", Priority.HIGH),
        ("Cancel subscription", "How to cancel auto-renewal?", Priority.MEDIUM),
    ],
    Category.SUPPORT: [  # ← FIXED: Added missing support templates
        ("How to use feature?", "Confused about dashboard analytics.", Priority.MEDIUM),
        ("General question", "Where do I find my reports?", Priority.LOW),
        ("Setup help", "Installation guide unclear.", Priority.MEDIUM),
    ],
    Category.SPAM: [
        ("FREE MONEY!!!", "Claim your $1M NOW!!! Click here!!!", Priority.LOW),
        ("WIN iPhone", "You won free iPhone 15! Verify now.", Priority.LOW),
    ]
}

def generate_emails(task_id: str, num_emails: int) -> List[Email]:
    """Generate realistic emails for task difficulty."""
    emails = []
    email_id = 1
    
    available_categories = list(Category)
    random.shuffle(available_categories)
    
    for i in range(num_emails):
        # Pick category (more bugs/billing for realism)
        cat = random.choices(
            available_categories, 
            weights=[0.2, 0.1, 0.15, 0.25, 0.25, 0.05][i%6]
        )[0]
        
        templates = TEMPLATES.get(cat, TEMPLATES[Category.SUPPORT])  # Safe fallback
        subject, body, priority = random.choice(templates)
        
        email = Email(
            id=f"email_{email_id}",
            subject=subject,
            body=body,
            sender=f"user{random.randint(1000,9999)}@customer.com",
            timestamp=f"2024-01-{random.randint(1,28):02d} {random.randint(9,17):02d}:00",
            priority=priority,
            category=cat
        )
        emails.append(email)
        email_id += 1
    
    random.shuffle(emails)
    return emails