import requests

API_KEY = "8d545211-fb9f-4aab-9534-8670cee35af9"
HOST = "book.dgeo.id"

url_list = [
    "https://book.dgeo.id/products/21-tips-mendidik-anak-berkebutuhan-khusus",
    "https://book.dgeo.id/products/21-tips-mendidik-anak-berkebutuhan-khusus/faq.html",
    "https://book.dgeo.id/products/21-tips-mendidik-anak-berkebutuhan-khusus/testimoni.html",
    "https://book.dgeo.id/products/21-tips-mendidik-anak-berkebutuhan-khusus/artikel.html",
    "https://book.dgeo.id/products/21-tips-mendidik-anak-berkebutuhan-khusus/galeri.html",
    "https://book.dgeo.id/products/muhammad-muda-gue-banget",
    "https://book.dgeo.id/products/muhammad-muda-gue-banget/faq.html",
    "https://book.dgeo.id/products/muhammad-muda-gue-banget/testimoni.html",
    "https://book.dgeo.id/products/muhammad-muda-gue-banget/artikel.html",
    "https://book.dgeo.id/products/muhammad-muda-gue-banget/galeri.html",
    "https://book.dgeo.id/products/penerbit-bypass",
    "https://book.dgeo.id/products/penerbit-bypass/faq.html",
    "https://book.dgeo.id/products/penerbit-bypass/testimoni.html",
    "https://book.dgeo.id/products/penerbit-bypass/artikel.html",
    "https://book.dgeo.id/products/penerbit-bypass/galeri.html",
    "https://book.dgeo.id/products/my-best-friend",
    "https://book.dgeo.id/products/my-best-friend/faq.html",
    "https://book.dgeo.id/products/my-best-friend/testimoni.html",
    "https://book.dgeo.id/products/my-best-friend/artikel.html",
    "https://book.dgeo.id/products/my-best-friend/galeri.html",
    "https://book.dgeo.id/products/ekonomi-pariwisata-dan-perhotelan",
    "https://book.dgeo.id/products/ekonomi-pariwisata-dan-perhotelan/faq.html",
    "https://book.dgeo.id/products/ekonomi-pariwisata-dan-perhotelan/testimoni.html",
    "https://book.dgeo.id/products/ekonomi-pariwisata-dan-perhotelan/artikel.html",
    "https://book.dgeo.id/products/ekonomi-pariwisata-dan-perhotelan/galeri.html",
    "https://book.dgeo.id/products/soekarno:-nasionalisme-untuk-tata-dunia-baru",
    "https://book.dgeo.id/products/soekarno:-nasionalisme-untuk-tata-dunia-baru/faq.html",
    "https://book.dgeo.id/products/soekarno:-nasionalisme-untuk-tata-dunia-baru/testimoni.html",
    "https://book.dgeo.id/products/soekarno:-nasionalisme-untuk-tata-dunia-baru/artikel.html",
    "https://book.dgeo.id/products/soekarno:-nasionalisme-untuk-tata-dunia-baru/galeri.html",
    "https://book.dgeo.id"
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