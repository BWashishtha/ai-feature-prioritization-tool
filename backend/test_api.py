import requests

url = "http://127.0.0.1:5000/api/prioritize"
data = {
    "features": [
        "User wants dark mode",
        "Export reports to CSV",
        "Enable two-factor authentication",
        "Faster page load times"
    ]
}

response = requests.post(url, json=data)

print(response.json())
