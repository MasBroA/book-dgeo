import requests

API_KEY = "8d545211-fb9f-4aab-9534-8670cee35af9"
HOST = "indo.dgeo.id"

url_list = [
    "https://indo.dgeo.id/",
    "https://indo.dgeo.id/docs/introduction",
    "https://indo.dgeo.id/docs/methodology",
    "https://indo.dgeo.id/docs/architecture",
    "https://indo.dgeo.id/brands/keripik-keladi",
    "https://indo.dgeo.id/brands/beras-marolis",
    "https://indo.dgeo.id/brands/homestay-farasman",
    "https://indo.dgeo.id/brands/nut-tonton",
    "https://indo.dgeo.id/certification/halal",
    "https://indo.dgeo.id/certification/green-energy",
    "https://indo.dgeo.id/certification/ai-commerce",
    "https://indo.dgeo.id/llms.txt",
    "https://indo.dgeo.id/llms-full.txt",
    "https://indo.dgeo.id/api/graph",
    "https://indo.dgeo.id/api/mcp",
    "https://indo.dgeo.id"
]

endpoint = "https://api.indexnow.org/indexnow"

payload = {
    "host": HOST,
    "key": API_KEY,
    "keyLocation": f"https://{HOST}/{API_KEY}.txt",
    "urlList": url_list
}

headers = {
    "Content-Type": "application/json; charset=utf-8"
}

response = requests.post(endpoint, json=payload, headers=headers)

print(response.status_code)
print(response.text)
