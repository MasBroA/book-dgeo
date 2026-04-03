import os
import json
import requests

def fetch_brands_from_api():
    api_url = "https://produk.dgeomart.com/api/publik/product/list_latest_update"
    try:
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Gagal ambil data API: {e}")
        return []

def create_markdown(product):
    directory = "directory"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = product.get('url_profile') or "https://www.dgeomart.com"
    contact_nama = product.get('contact_nama') or ""
    contact_telp = product.get('contact_telp') or ""
    contact_email = product.get('contact_email') or ""
    
    # Konversi koordinat ke float (API memberikan string)
    try:
        lat = float(product.get('latitude', 0))
        long = float(product.get('longitude', 0))
    except (ValueError, TypeError):
        lat, long = 0.0, 0.0

    # Skema JSON-LD (Sangat penting untuk GEO Optimizer)
    json_ld = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{nama}",
  "kontak": "{contact_nama} - {contact_telp} - {contact_email}",
  "description": "{deskripsi} {catatan}",
  "url": "{url_link}",
  "image": "{product.get('url_foto_profile')}",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "{product.get('alamat')}",
    "addressLocality": "{wilayah}",
    "addressCountry": "ID"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": {lat},
    "longitude": {long}
  }}
}}
</script>
"""

    content = f"""---
title: "{nama} - {wilayah}"
last_updated: "{product.get('updated_time')}"
---
{json_ld}

# {nama}

**Lokasi:** {wilayah}  
**Alamat:** {product.get('alamat')}

### Deskripsi
{deskripsi}

{catatan}


---
### Informasi Tambahan
* **Kontak:** {product.get('contact_nama')} - {product.get('contact_telp')} - {product.get('contact_email')} 
* **Terakhir Update:** {product.get('updated_time')}

[Informasi selengkapnya di ] ({url_link})

[Dapatkan informasi lainnya di] DGeomart - https://www.dgeomart.com 

![QR Code]({product.get('qr_link')})
"""

    # Gunakan slug dari API untuk nama file
    slug = product.get('slug') or f"product-{product.get('product_id')}"
    filename = f"{directory}/{slug}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Berhasil membuat: {filename}")

def generate_sitemap():
    base_url = "https://masbroa.github.io/Lokal-Brand-Index/directory/"
    files = os.listdir("directory")

    with open("sitemap.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://sitemaps.org">\n')
        for file in files:
            if file.endswith(".md"):
                 # MENGHAPUS ekstensi .md dari URL
                clean_name = file.replace(".md", "")

                f.write(f'  <url>\n    <loc>{base_url}{clean_name}</loc>\n  </url>\n')
        f.write('</urlset>')
    print("✅ Sitemap.xml updated")

# --- EKSEKUSI UTAMA ---
print("🚀 Memulai sinkronisasi data dari API DGeomart...")
products = fetch_brands_from_api()

if products:
    for item in products:
        create_markdown(item)
    generate_sitemap()
    print(f"🎉 Selesai! Total {len(products)} produk diproses.")
else:
    print("⚠️ Tidak ada data yang diterima dari API.")
