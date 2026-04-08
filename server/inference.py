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
    # [START] Log
    print(f"[START] {{\"task_id\": \"{task_id}\", \"model\": \"{MODEL_NAME}\"}}")
    
    try:
        requests.post(f"{ENV_URL}/reset")
        total_reward = 0

        for i, action_data in enumerate(actions):
            step_req = requests.post(f"{ENV_URL}/step", json=action_data)
            res_obs, res_reward, done, info = step_req.json()
            
            total_reward += res_reward['value']
            
            # [STEP] Log
            step_log = {"step": i, "action": action_data, "reward": res_reward['value'], "done": done}
            print(f"[STEP] {json.dumps(step_log)}")
            
            if done: break

        # [END] Log
        print(f"[END] {{\"final_score\": {round(total_reward, 2)}}}")
        
    except Exception as e:
        print(f"Error in {task_id}: {e}")

if __name__ == "__main__":
    # LEVEL 1: EASY (Just Classify)
    run_task("triage_basics_v1", [
        {"action_type": "classify", "ticket_id": "T1", "category": "technical"}
    ])

    # LEVEL 2: MEDIUM (Classify + Prioritize)
    run_task("vip_priority_v1", [
        {"action_type": "classify", "ticket_id": "T3", "category": "technical"},
        {"action_type": "prioritize", "ticket_id": "T3", "priority": 4}
    ])

    # LEVEL 3: HARD (Classify + Prioritize + Resolve)
    run_task("full_resolve_v1", [
        {"action_type": "classify", "ticket_id": "T1", "category": "billing"},
        {"action_type": "prioritize", "ticket_id": "T1", "priority": 4},
        {"action_type": "resolve", "ticket_id": "T1", "resolution_summary": "Processed refund for duplicate charge."}
    ])