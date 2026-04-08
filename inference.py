import os
import json
import requests
from openai import OpenAI

# Required Env Vars
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4o")
HF_TOKEN = os.environ.get("HF_TOKEN")

# YOUR DIRECT HF SPACE URL
ENV_URL = "https://maku1234-openenv.hf.space" 

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

def run_task(task_id, actions):
    print(f"[START] {{\"task_id\": \"{task_id}\", \"model\": \"{MODEL_NAME}\"}}")
    
    try:
        requests.post(f"{ENV_URL}/reset")
        total_reward = 0
        
        for i, action_data in enumerate(actions):
            step_req = requests.post(f"{ENV_URL}/step", json=action_data)
            
            # The environment returns a list: [obs, reward, done, info]
            response_data = step_req.json()
            res_reward = response_data[1]
            done = response_data[2]
            
            reward_value = res_reward.get('value', 0.0) if isinstance(res_reward, dict) else res_reward
            total_reward += reward_value
            
            step_log = {"step": i, "action": action_data, "reward": round(reward_value, 2), "done": done}
            print(f"[STEP] {json.dumps(step_log)}")
            
            if done: break
            
        print(f"[END] {{\"final_score\": {round(total_reward, 2)}}}")
            
    except Exception as e:
        print(f"Error in {task_id}: {e}")

if __name__ == "__main__":
    # Task 1: Easy
    run_task("triage_basics_v1", [{"action_type": "classify", "ticket_id": "T1", "category": "technical"}])
    
    # Task 2: Medium
    run_task("vip_priority_v1", [
        {"action_type": "classify", "ticket_id": "T3", "category": "technical"},
        {"action_type": "prioritize", "ticket_id": "T3", "priority": 4}
    ])
    
    # Task 3: Hard
    run_task("full_resolve_v1", [
        {"action_type": "classify", "ticket_id": "T1", "category": "billing"},
        {"action_type": "prioritize", "ticket_id": "T1", "priority": 4},
        {"action_type": "resolve", "ticket_id": "T1", "resolution_summary": "Processed refund."}
    ])
