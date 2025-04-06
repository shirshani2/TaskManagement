from openai import OpenAI
import os
import json
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_task_description(description):
    prompt = f"""You are a smart assistant that receives a task description and returns:
1. Category (e.g., work, study, personal, urgent, shopping, etc.) in hebrew
2. Estimated time to complete (in hours). in hebrew 

Task: {description}
Return a short JSON object with keys 'category' and 'time_estimate'."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content
    return json.loads(content)  
