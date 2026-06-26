import requests

url = "http://127.0.0.1:8000/query"
payload = {"repository": "ACIS", "query": "what is SPAposition?"}
response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"Raw Bytes (first 50): {response.content[:50]}")
print(f"Raw Text (first 200): {response.text[:200]}")
