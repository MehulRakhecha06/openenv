import os
import sys
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

# Fix imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.env import EmailTriageEnv
from src.models import Action

load_dotenv()

def run_baseline(model="gpt-3.5-turbo", task_id="easy", max_steps=100):
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Set OPENAI_API_KEY environment variable!")
        return 0.0
    
    client = OpenAI()
    env = EmailTriageEnv(task_id)
    obs, info = env.reset()
    
    total_reward = 0.0
    step = 0
    
    print(f"🚀 Running {task_id} task (max {max_steps} steps)...")
    
    while step < max_steps:
        prompt = f"""
Task: {info.task_id} | Inbox: {len(env.inbox)} emails

CURRENT EMAIL:
{obs.current_email.model_dump_json() if obs.current_email else "No email"}

Stats: {obs.stats}

ACTIONS (JSON only):
{{"type": "classify", "email_id": "email_X", "priority": "high", "category": "bug"}}
{{"type": "next"}}
{{"type": "skip", "email_id": "email_X"}}
"""
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=150
            )
            
            # Parse action safely
            action_str = response.choices[0].message.content.strip()
            action_dict = json.loads(action_str) if action_str.startswith('{') else {"type": "next"}
            
            obs, reward, done, truncated, info = env.step(action_dict)
            total_reward += reward
            
            print(f"Step {step+1}: {action_dict} | Reward: {reward:+.2f} | Total: {total_reward:.2f}")
            
            if done or truncated:
                break
                
        except Exception as e:
            print(f"Error: {e} -> defaulting to 'next'")
            obs, reward, truncated, done, info = env.step({"type": "next"})
            total_reward += reward
        
        step += 1
        time.sleep(0.5)
    
    final_score = env.grader.grade_task(env.processed_emails, env.true_emails, env.task_config)
    
    print(f"\n✅ FINAL {task_id.upper()}: {final_score:.3f}")
    return final_score

if __name__ == "__main__":
    tasks = ["easy", "medium", "hard"]
    scores = {}
    
    for task in tasks:
        scores[task] = run_baseline(task_id=task, max_steps={"easy":25, "medium":50, "hard":100}[task])
    
    print("\n" + "="*60)
    print("BASELINE SCORES")
    print("="*60)
    for task, score in scores.items():
        print(f"{task:>8}: {score:.3f}")