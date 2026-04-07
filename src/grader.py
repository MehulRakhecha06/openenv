from typing import Dict, Any, List
from .models import Priority, Category

class EmailTriageGrader:
    """Deterministic grader: 0.0-1.0 score per task."""
    
    PRIORITY_WEIGHTS = {
        Priority.LOW: 0.25,
        Priority.MEDIUM: 0.5,
        Priority.HIGH: 0.75,
        Priority.URGENT: 1.0
    }
    
    def grade_task(self, processed_emails: List[Dict], true_emails: Dict[str, Any], task_config: Dict) -> float:
        """Grade performance 0.0-1.0."""
        total_emails = task_config["num_emails"]
        completed_emails = [e for e in processed_emails if e.get("completed")]
        processed_count = len(completed_emails)
        
        if processed_count == 0:
            return 0.0
        
        # Progress score (0-1)
        progress_score = processed_count / total_emails
        
        # Accuracy score for completed emails
        accuracy_score = 0.0
        for processed in completed_emails:
            email_id = processed["email_id"]
            if email_id in true_emails:
                true_data = true_emails[email_id]
                
                # Priority accuracy (partial credit)
                pred_priority = processed.get("priority")
                true_priority = true_data["priority"]
                if pred_priority == true_priority:
                    priority_score = 1.0
                else:
                    priority_score = self.PRIORITY_WEIGHTS.get(pred_priority, 0.0) / self.PRIORITY_WEIGHTS[true_priority]
                
                # Category accuracy (binary)
                category_score = 1.0 if processed.get("category") == true_data["category"] else 0.0
                
                accuracy_score += (priority_score + category_score) / 2
        
        accuracy_score /= processed_count
        
        # Weighted final score
        final_score = 0.6 * progress_score + 0.4 * accuracy_score
        return min(1.0, final_score)