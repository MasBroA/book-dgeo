import requests

API_KEY = "8d545211-fb9f-4aab-9534-8670cee35af9"
HOST = "www.dgeo.id"

url_list = [
    "https://www.dgeo.id/"
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
