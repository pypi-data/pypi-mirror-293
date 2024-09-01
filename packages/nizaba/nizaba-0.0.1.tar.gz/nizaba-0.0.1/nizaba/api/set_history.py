import os
import requests
import json

from datetime import datetime

def set_history(data):
    
    NZB_API_KEY = os.getenv("NZB_API_KEY")

    headers = {"Authorization": NZB_API_KEY}
    request_data = {
        "data": json.dumps(data),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        print("Sending request to https://api.nizaba.com/api/set_history")
        response = requests.post("https://api.nizaba.com/api/set_history", headers=headers, json=request_data)
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return
        
    except Exception as e:
        print(f"Error: {e}")
        return