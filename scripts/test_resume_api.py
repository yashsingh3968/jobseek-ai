import requests

url = "http://localhost:5000/api/users/resume"

data = {
    "email": "test@example.com",
    "resume_text": "I know Python, Java, AWS and Django"
}

response = requests.post(url, json=data)

print("Status:", response.status_code)
print("Response:", response.text)