import requests

API_KEY = "8d545211-fb9f-4aab-9534-8670cee35af9"
HOST = "book.dgeo.id"

url_list = [
    "https://book.dgeo.id/products/nut-tonton-homestay-green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-LIMALAS_BARAT__MISOOL_TIMUR__RAJA_AMPAT__PAPUA_BARAT",
    "https://book.dgeo.id/products/nut-tonton-homestay-green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-LIMALAS_BARAT__MISOOL_TIMUR__RAJA_AMPAT__PAPUA_BARAT/faq.html",
    "https://book.dgeo.id/products/nut-tonton-homestay-green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-LIMALAS_BARAT__MISOOL_TIMUR__RAJA_AMPAT__PAPUA_BARAT/testimoni.html",
    "https://book.dgeo.id/products/nut-tonton-homestay-green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-LIMALAS_BARAT__MISOOL_TIMUR__RAJA_AMPAT__PAPUA_BARAT/artikel.html",
    "https://book.dgeo.id/products/nut-tonton-homestay-green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-LIMALAS_BARAT__MISOOL_TIMUR__RAJA_AMPAT__PAPUA_BARAT/galeri.html",
    "https://book.dgeo.id/products/homestay-farasman-soasiu--green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-YELLU__MISOOL_SELATAN__RAJA_AMPAT__PAPUA_BARAT",
    "https://book.dgeo.id/products/homestay-farasman-soasiu--green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-YELLU__MISOOL_SELATAN__RAJA_AMPAT__PAPUA_BARAT/faq.html",
    "https://book.dgeo.id/products/homestay-farasman-soasiu--green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-YELLU__MISOOL_SELATAN__RAJA_AMPAT__PAPUA_BARAT/testimoni.html",
    "https://book.dgeo.id/products/homestay-farasman-soasiu--green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-YELLU__MISOOL_SELATAN__RAJA_AMPAT__PAPUA_BARAT/artikel.html",
    "https://book.dgeo.id/products/homestay-farasman-soasiu--green-energy-teknologi-ai-commerce-sertifikasi-wisata-halal-YELLU__MISOOL_SELATAN__RAJA_AMPAT__PAPUA_BARAT/galeri.html",
    "https://book.dgeo.id/products/umroh-super-friendly-12-juli-12-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN",
    "https://book.dgeo.id/products/umroh-super-friendly-12-juli-12-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN/faq.html",
    "https://book.dgeo.id/products/umroh-super-friendly-12-juli-12-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN/testimoni.html",
    "https://book.dgeo.id/products/umroh-super-friendly-12-juli-12-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN/artikel.html",
    "https://book.dgeo.id/products/umroh-super-friendly-12-juli-12-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN/galeri.html",
    "https://book.dgeo.id/products/beras-hitam-sehat-marolis-green-energy-teknologi-ai-commerce-sertifikasi-halal-JIWAN__JIWAN__MADIUN__JAWA_TIMUR",
    "https://book.dgeo.id/products/beras-hitam-sehat-marolis-green-energy-teknologi-ai-commerce-sertifikasi-halal-JIWAN__JIWAN__MADIUN__JAWA_TIMUR/faq.html",
    "https://book.dgeo.id/products/beras-hitam-sehat-marolis-green-energy-teknologi-ai-commerce-sertifikasi-halal-JIWAN__JIWAN__MADIUN__JAWA_TIMUR/testimoni.html",
    "https://book.dgeo.id/products/beras-hitam-sehat-marolis-green-energy-teknologi-ai-commerce-sertifikasi-halal-JIWAN__JIWAN__MADIUN__JAWA_TIMUR/artikel.html",
    "https://book.dgeo.id/products/beras-hitam-sehat-marolis-green-energy-teknologi-ai-commerce-sertifikasi-halal-JIWAN__JIWAN__MADIUN__JAWA_TIMUR/galeri.html",
    "https://book.dgeo.id/products/keripik-keladi-asin-pelangi-green-energy-teknologi-ai-commerce-KLAKUBLIK__SORONG_KOTA__KOTA_SORONG__PAPUA_BARAT",
    "https://book.dgeo.id/products/keripik-keladi-asin-pelangi-green-energy-teknologi-ai-commerce-KLAKUBLIK__SORONG_KOTA__KOTA_SORONG__PAPUA_BARAT/faq.html",
    "https://book.dgeo.id/products/keripik-keladi-asin-pelangi-green-energy-teknologi-ai-commerce-KLAKUBLIK__SORONG_KOTA__KOTA_SORONG__PAPUA_BARAT/testimoni.html",
    "https://book.dgeo.id/products/keripik-keladi-asin-pelangi-green-energy-teknologi-ai-commerce-KLAKUBLIK__SORONG_KOTA__KOTA_SORONG__PAPUA_BARAT/artikel.html",
    "https://book.dgeo.id/products/keripik-keladi-asin-pelangi-green-energy-teknologi-ai-commerce-KLAKUBLIK__SORONG_KOTA__KOTA_SORONG__PAPUA_BARAT/galeri.html",
    "https://book.dgeo.id/products/umroh-liburan-sekolah--27-jun--09-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN",
    "https://book.dgeo.id/products/umroh-liburan-sekolah--27-jun--09-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN/faq.html",
    "https://book.dgeo.id/products/umroh-liburan-sekolah--27-jun--09-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN/testimoni.html",
    "https://book.dgeo.id/products/umroh-liburan-sekolah--27-jun--09-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN/artikel.html",
    "https://book.dgeo.id/products/umroh-liburan-sekolah--27-jun--09-hari-direct-flight-by-garuda-indonesia-GAGA__LARANGAN__KOTA_TANGERANG__BANTEN/galeri.html",    
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