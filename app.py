import gradio as gr
from src.env import EmailTriageEnv
import json

def run_demo(task_id, model_prompt):
    env = EmailTriageEnv(task_id)
    obs, _ = env.reset()
    
    return {
        "task": task_id,
        "current_email": obs.current_email.model_dump_json(indent=2) if obs.current_email else "No email",
        "stats": obs.stats,
        "suggested_action": json.dumps({
            "type": "classify", 
            "email_id": obs.current_email.id if obs.current_email else None,
            "priority": "high",
            "category": "bug"
        }, indent=2)
    }

demo = gr.Interface(
    fn=run_demo,
    inputs=[
        gr.Dropdown(["easy", "medium", "hard"], label="Task", value="easy"),
        gr.Textbox("Enter your model reasoning here...", label="Model Reasoning")
    ],
    outputs=gr.JSON(label="Environment State"),
    title="📧 Email Triage OpenEnv Demo",
    description="Test the email triage environment!"
)

if __name__ == "__main__":
    demo.launch()