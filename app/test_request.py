import requests

url = "http://127.0.0.1:5000/api/users"
data = {"name": "Shir"}  # 🔥 הגדרה של JSON שנשלח לשרת

response = requests.post(url, json=data)

print("Status code:", response.status_code)
print("Raw text:", response.text)
