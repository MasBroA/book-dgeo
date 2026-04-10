import requests

API_KEY = "YOUR_API_KEY"
HOST = "green.dgeo.id"

url_list = [
    "https://domain.com/directory/produk-1",
    "https://domain.com/directory/produk-2"
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