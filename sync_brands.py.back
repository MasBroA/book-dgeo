import os
import json
import requests

from datetime import date
from datetime import datetime

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
    url_link = product.get('url_profile') or "https://green.dgeo.id"
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
Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk

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

    print(f"✅ Berhasil membuat markdown: {filename}")

def create_markdown_html(product):
    directory = "directory"
    if not os.path.exists(directory):
        os.makedirs(directory)


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = product.get('url_profile') or "https://green.dgeo.id"
    contact_nama = product.get('contact_nama') or ""
    contact_telp = product.get('contact_telp') or ""
    contact_email = product.get('contact_email') or ""
    
    # Konversi koordinat ke float (API memberikan string)
    try:
        lat = float(product.get('latitude', 0))
        long = float(product.get('longitude', 0))
    except (ValueError, TypeError):
        lat, long = 0.0, 0.0

    org_product_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://green.dgeo.id",
                "name": "DGeomart",
                "url": "https://green.dgeo.id",
                "logo": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "sameAs": [
                    "https://instagram.com",
                    "https://wa.me"
                ]
            },
            {
                "@type": "Website",
                "name": "Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified",
                "image": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "description": "Platform indeks brand lokal terpercaya untuk Sustainable Local Growth...",
                "brand": {
                    "@type": "Brand",
                    "name": "DGeomart"
                }                
            }
        ]
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Apa standar brand yang masuk dalam Lokal Brand Index?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Brand harus memenuhi minimal satu dari tiga kriteria: memiliki sertifikasi halal (produk/wisata), menggunakan energi bersih/ramah lingkungan dalam proses produksi, atau mengintegrasikan teknologi AI dalam layanan konsumen."
                }
            }
        ]
    }

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <!-- Meta Dasar -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="mkts7AhE-ySL6g37ibn9s4Am0HWwEzPyo8cZ2UA_Rdc" />
    <meta name="robots" content="index, follow">
    <meta name="author" content="DGeoId">
    <meta name="theme-color" content="#0f172a">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified</title>
    <meta name="description" content="Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk">
    <meta name="keywords" content="Brand Lokal, Sertifikasi Halal, Green Energy Indonesia, Energi Hijau, Teknologi AI, AI Verified, Produk Ramah Lingkungan, Wisata Halal">
    <link rel="canonical" href="https://green.dgeo.id/">

    <!-- Open Graph (Sosial Media) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified">
    <meta property="og:description" content="Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk">
    <meta property="og:url" content="https://green.dgeo.id/">
    <meta property="og:image" content="https://green.dgeo.id/images/logo-dgeo-id.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">

        <!-- Favicon -->
    <link rel="icon" href="https://green.dgeo.id/images/logo-dgeo-id.png" type="image/x-icon">




    <!-- JSON-LD Schema: Dioptimalkan untuk Rich Snippets (Bintang Kuning) -->
    <script type="application/ld+json">
    {json.dumps(org_product_schema, indent=2)}
    </script>

    <!-- 2. SCHEMA FAQ (Memudahkan AI Menjawab Pertanyaan User) -->
    <script type="application/ld+json">
        {json.dumps(faq_schema, indent=2)}
    </script>

    <link href="/css/green-general.css" rel="stylesheet" />
    <link rel="alternate" hreflang="id" href="https://green.dgeo.id/">
</head>
<body>
    <!-- Header & Hero -->
    <header class="hero">
        <img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo">
        <span class="slogan">Smart Indexing for Sustainable Local Growth, Green Energy, AI Verified and Halal Certified</span>
        <h1>Platform index lokal produk yang Green Energy Verified, Halal Certified dan AI Verified</h1>
        <p>Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk</p>
        
    </header>

    <!-- Katalog Section -->
    <main class="container">
        <div class="section-header">
<center>
<h2>title: "{nama} - {wilayah}"</h2>
<h3>Lokasi:{wilayah}</h3>
<h3>Alamat: {product.get('alamat')}</h3>
<h4>last_updated: "{product.get('updated_time')}"</h4>
</center>
        </div>
        <div class="section-header">
<p>{deskripsi}</p>

<p>{catatan}</p>
        </div>

        <div class="section-header">
<p>Kontak:<br>
{product.get('contact_nama')} - {product.get('contact_telp')} - {product.get('contact_email')}</p> 
<p>Terakhir Update: {product.get('updated_time')}</p>

<p>Informasi selengkapnya di ] ({url_link})</p>

<p>Dapatkan informasi lainnya di DGeomart - https://www.dgeomart.com</p> 

<p>{product.get('qr_link')}</p>
        </section>
    </main>
    <footer>
        <div class="footer-nav">
            <a href="#">Tentang</a>
            <a href="#">Privasi</a>
            <a href="#">Kontak</a>
            <a href="https://instagram.com">Instagram</a>
        </div>
        <p class="copy">&copy; 2024 DGeoGreen  - Smart Indexing for Sustainable Local Growth. All rights reserved.</p>
    </footer>

</body>
</html>"""

    # Gunakan slug dari API untuk nama file
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"

    folder_path = f"{directory}/{slug}-{wilayah_name}"

    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{folder_path}/index.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)


    print(f"✅ Berhasil membuat: {filename}")

def generate_sitemap():
    base_url = "https://masbroa.github.io/Lokal-Brand-Index/directory/"
    files = os.listdir("directory")
    today = date.today()
    now = datetime.now()

    with open("sitemap.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        # PERBAIKAN: Namespace harus lengkap seperti di bawah ini
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        #f.write('<urlset xmlns="http://sitemaps.org">\n')
        for file in files:
            if file.endswith(".md"):
                 # MENGHAPUS ekstensi .md dari URL
                clean_name = file.replace(".md", "")

                f.write(f'  <url>\n    <loc>{base_url}{clean_name}</loc>\n    <lastmod>{now}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
        f.write('</urlset>')
    print("✅ Sitemap.xml updated")

# --- EKSEKUSI UTAMA ---
print("🚀 Memulai sinkronisasi data dari API DGeomart...")
products = fetch_brands_from_api()

if products:
    for item in products:
        create_markdown(item)
    for item in products:
        create_markdown_html(item)        
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

        url_link = p['url_profile'] or "https://green.dgeo.id"
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
        list_html += f'<li><a href="./directory/{slug}-{wilayah_name}/">{p["nama"]} - {p["wilayah_nama"]}</a><p>{p["deskripsi"]}</p></li>\n'

    # Gabungkan ke Template
    json_ld_list = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": items_json
    }, indent=2)

    item_list_schema = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": items_json
    }
    org_product_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://green.dgeo.id",
                "name": "DGeomart",
                "url": "https://green.dgeo.id",
                "logo": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "sameAs": [
                    "https://instagram.com",
                    "https://wa.me"
                ]
            },
            {
                "@type": "Website",
                "name": "Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified",
                "image": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "description": "Platform indeks brand lokal terpercaya untuk Sustainable Local Growth...",
                "brand": {
                    "@type": "Brand",
                    "name": "DGeomart"
                }
            }
        ]
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Apa standar brand yang masuk dalam Lokal Brand Index?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Brand harus memenuhi minimal satu dari tiga kriteria: memiliki sertifikasi halal (produk/wisata), menggunakan energi bersih/ramah lingkungan dalam proses produksi, atau mengintegrasikan teknologi AI dalam layanan konsumen."
                }
            }
        ]
    }

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <!-- Meta Dasar -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta charset="UTF-8">
    <meta name="google-site-verification" content="mkts7AhE-ySL6g37ibn9s4Am0HWwEzPyo8cZ2UA_Rdc" />
    <meta name="robots" content="index, follow">
    <meta name="author" content="DGeoId">
    <meta name="theme-color" content="#0f172a">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified</title>
    <meta name="description" content="Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk">
    <meta name="keywords" content="Brand Lokal, Sertifikasi Halal, Green Energy Indonesia, Energi Hijau, Teknologi AI, AI Verified, Produk Ramah Lingkungan, Wisata Halal">
    <link rel="canonical" href="https://green.dgeo.id/">

    <!-- Open Graph (Sosial Media) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified">
    <meta property="og:description" content="Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk">
    <meta property="og:url" content="https://green.dgeo.id/">
    <meta property="og:image" content="https://green.dgeo.id/images/logo-dgeo-id.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">

    <!-- Favicon -->
    <link rel="icon" href="https://green.dgeo.id/images/logo-dgeo-id.png" type="image/x-icon">



    <!-- JSON-LD Schema: Dioptimalkan untuk Rich Snippets (Bintang Kuning) -->
    <script type="application/ld+json">
    {json.dumps(org_product_schema, indent=2)}
    </script>

    <!-- 2. SCHEMA FAQ (Memudahkan AI Menjawab Pertanyaan User) -->
    <script type="application/ld+json">
        {json.dumps(faq_schema, indent=2)}
    </script>

    <!-- SKEMA DAFTAR ITEM (Naikkan Skor Discovery) -->
    <script type="application/ld+json">
        {json.dumps(item_list_schema, indent=2)}
    </script>
	<link href="/css/green-general.css" rel="stylesheet" />
    <link rel="alternate" hreflang="id" href="https://green.dgeo.id/">

</head>
<body>
    <!-- Header & Hero -->
    <header class="hero">
        <img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo">
        <span class="slogan">Smart Indexing for Sustainable Local Growth, Green Energy, AI Verified and Halal Certified</span>
        <h1>Platform index lokal produk yang Green Energy Verified, Halal Certified dan AI Verified</h1>
        <p>Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk</p>
        
        <div class="search-container">
            <input type="text" class="search-input" placeholder="Cari brand kuliner, fashion, atau teknologi lokal...">
        </div>

        <div class="rating-badge">
            <span class="stars">★★★★★</span> 
            <strong>4.9/5</strong> 
            <small style="margin-left: 10px; color: #666;">(1.250+ Ulasan Terverifikasi)</small>
        </div>
    </header>

    <!-- Katalog Section -->
    <main class="container">
        <div class="section-header">
            <h2>Katalog Brand Pilihan</h2>
            <p>Menampilkan brand lokal yang telah lulus kurasi Green Energy, ramah lingkungan, Sertifikasi Halal dan standar AI.</p>
        </div>
        <section id="directory">
            <h2>Direktori Brand & Lokasi</h2>
            <article>
                <ul>{list_html}</ul>
            </article>
        </section>
    </main>
</body>
</html>"""


    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html updated with ItemList Schema")

update_index_html(products)
