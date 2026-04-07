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
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"
    filename = f"{directory}/{slug}-{wilayah_name}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    folder_path = f"{directory}/{slug}-{wilayah_name}"

    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{folder_path}/index.html"

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

def update_index_html(products):
    # Buat daftar link untuk HTML dan JSON-LD
    items_json = []
    list_html = ""
    
    for i, p in enumerate(products):
        wilayah = p['wilayah_nama'] or "Indonesia"
        url_link = p['url_profile'] or "https://www.dgeomart.com"
        #url = f"{p['url_profile']}"
        slug = p['slug'] or f"product-{p['product_id']}"

        wilayah_name = wilayah.replace(",", "_")
        wilayah_name = wilayah_name.replace(" ", "_")
        wilayah_name = wilayah_name.replace("'", "")

        items_json.append({
            "@type": "ListItem",
            "position": i + 1,
            "url": url_link,
            "name": p['nama']
        })
        list_html += f'<li><a href="./directory/{slug}-{wilayah_name}.md">{p["nama"]} - {p["wilayah_nama"]}</a></li>\n'

    # Gabungkan ke Template
    json_ld_list = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": items_json
    }, indent=2)

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <!-- Meta Dasar -->
    <meta name="description" content="Indeks Brand Lokal Indonesia untuk optimasi GEO dan penemuan produk UMKM.">
    <link rel="canonical" href="https://masbroa.github.io/Lokal-Brand-Index/">

    <!-- Open Graph (Sosial Media) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Lokal Brand Index - DGeomart">
    <meta property="og:description" content="Kumpulan direktori brand lokal dari berbagai wilayah di Indonesia.">
    <meta property="og:url" content="https://masbroa.github.io/Lokal-Brand-Index/">

    <!-- Favicon -->
    <link rel="icon" href="https://www.dgeomart.com/ecom/images/logo/logo2.png" type="image/x-icon">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="mkts7AhE-ySL6g37ibn9s4Am0HWwEzPyo8cZ2UA_Rdc" />
    <title>Lokal Brand Index - DGeomart GEO Optimizer</title>
    
    <!-- SKEMA ORGANISASI (Naikkan Skor Organization) -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "DGeomart",
      "url": "https://www.dgeomart.com",
      "logo": "https://www.dgeomart.com/ecom/images/logo/logo2.png"
    }}
    </script>

    <!-- SKEMA DAFTAR ITEM (Naikkan Skor Discovery) -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "itemListElement": {json.dumps(items_json)}
    }}
    </script>
</head>
<body>
    <main>
        <h1>Indeks Lokasi Brand Lokal (GEO)</h1>
        <ul>{list_html}</ul>
    </main>
</body>
</html>"""


    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html updated with ItemList Schema")

update_index_html(products)
