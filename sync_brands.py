import os
import json
import requests
import shutil

from pathlib import Path
from datetime import datetime, timezone, date

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
    directory = "products"
    if not os.path.exists(directory):
        os.makedirs(directory)

    items_faq = []
    list_faq=""
    list_artikel=""
    list_testimoni=""

    for i, a in enumerate(product['FAQ']):
        items_faq.append({
            "@type": "Question",
            "name": a["judul"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a["short_desc"]
            }
        })
        list_faq += f'- Q:{a["judul"]}\n  A:{a["short_desc"]}\n\n---\n'

    for i, a in enumerate(product['ARTIKEL']):
        list_artikel += f'- 📄 {a["judul"]}\n{a["deskripsi"]}\n\n---\n'

    for i, a in enumerate(product['TESTIMONI']):
        list_testimoni += f'- 📄 {a["short_desc"]}\n{a["by_nama"]}, {a["by_jabatan"]}, {a["by_alamat"]}\n\n---\n'


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    short_desc =  product.get('short_desc') or product.get('deskripsi') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" #product.get('url_profile') or "https://green.dgeo.id"
    url_foto_profile = product.get('url_foto_profile') or "https://green.dgeo.id/images/logo-dgeo-id.png"
    contact_nama = product.get('contact_nama') or ""
    contact_telp = product.get('contact_telp') or ""
    contact_email = product.get('contact_email') or ""

    # Gunakan slug dari API untuk nama file
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"

    folder_path = f"{directory}/{slug}-{wilayah_name}"
    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{directory}/{slug}-{wilayah_name}/README.md"

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
  "description": "{short_desc} {catatan}",
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

    content = f"""# 🇮🇩 Indeks Merek Lokal (Lokal Brand Index)

**Indeks Merek Lokal** adalah direktori terstruktur berbasis lokasi yang mengedepankan dukungan terhadap energi hijau (~energi terbarukan), ramah lingkungan, dengan memenuhi sertifikasi halal MUI, yang dirancang untuk meningkatkan visibilitas merek lokal Indonesia dalam ekosistem *Generative Engine Optimization (GEO)*.

---
{json_ld}

---
title: "{nama} - {wilayah}"

**Lokasi:** {wilayah}  

**Alamat:** {product.get('alamat')}

**Koordinat:**
- Latitude: {product.get('latitude')}
- Longitude: {product.get('longitude')}

last_updated: "{product.get('updated_time')}"
---
## Ringkasan
{deskripsi}

---
## Tentang produk/brand ini
{catatan}

## 📞 Kontak
- Nama: {product.get('contact_nama')}
- Telepon: {product.get('contact_telp')}
- Email: {product.get('contact_email')}

## 🔗 Link Terkait

- 🌐 Logo Produk/Brand:
  ({url_foto_profile})

- 🌐 Website resmi:
  ({url_link})

- 📄 Halaman produk:
  https://green.dgeo.id/{directory}/{slug}-{wilayah_name}/

---
## FAQ
{list_faq}

---
## Artikel Terkait
{list_artikel}

---
## Testimoni
{list_testimoni}

---
- 🔙 Kembali ke indeks:
  https://green.dgeo.id

---

## 🔍 Transparansi & Sumber Data
Data dalam halaman ini merupakan bagian dari sistem indeks brand lokal berbasis lokasi yang dikelola oleh DGeo Green.

---

## 🧭 Lihat juga
- [Indeks utama](/README.md)

"""

    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Berhasil membuat markdown: {filename}")

def create_index_html(product):
    directory = "products"
    if not os.path.exists(directory):
        os.makedirs(directory)

    items_faq = []
    list_faq=""
    list_artikel=""
    list_testimoni=""

    for i, a in enumerate(product['FAQ']):
        items_faq.append({
            "@type": "Question",
            "name": a["judul"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a["short_desc"]
            }
        })
        list_faq += f'<p>Q:{a["judul"]}<br>A:{a["short_desc"]}</p>'

    for i, a in enumerate(product['ARTIKEL']):
        list_artikel += f'<p><b>{a["judul"]}</b><br>A:{a["deskripsi"]}</p>'

    for i, a in enumerate(product['TESTIMONI']):
        list_testimoni += f'<p><i>{a["short_desc"]}</i><br>{a["by_nama"]}, {a["by_jabatan"]}, {a["by_alamat"]}</p>'


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    short_desc =  product.get('short_desc') or product.get('deskripsi') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" # product.get('url_profile') or "https://green.dgeo.id"
    url_foto_profile = product.get('url_foto_profile') or "https://green.dgeo.id/images/logo-dgeo-id.png"
    keyword = product.get('keyword') or ""
    tagline = product.get('tagline') or ""
    rating = product.get('rating') or "5"

    # Gunakan slug dari API untuk nama file
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"

    folder_path = f"{directory}/{slug}-{wilayah_name}"

    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{folder_path}/index.html"

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
                "name": "DGeo Green",
                "url": "https://green.dgeo.id",
                "logo": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "sameAs": [
                    "https://github.com/MasBroA/Lokal-Brand-Index"
                ]
            },
            {
                "@type": "Website",
                "name": nama,
                "image": url_foto_profile,
                "description": short_desc,
                "brand": {
                    "@type": "Brand",
                    "name": nama
                }                
            }
        ]
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items_faq
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
    <title>{nama}</title>
    <meta name="description" content="{short_desc}">
    <meta name="keywords" content="{keyword}">
    <link rel="canonical" href="https://green.dgeo.id/">

    <!-- Open Graph (Sosial Media) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{nama}">
    <meta property="og:description" content="{short_desc}">
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
        <a href="https://green.dgeo.id"><img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
        <span class="slogan">{tagline}</span>
        <h1>{nama}</h1>
        <p>{deskripsi}<br>{catatan}</p>
        
        <a href="https://green.dgeo.id/{folder_path}/index.html"><img src="{url_foto_profile}" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
    </header>

    <!-- Katalog Section -->
    <main class="container">

        <div class="section-header">
            <center>
            <h3>Lokasi:{wilayah}</h3>
            <h3>Alamat: {product.get('alamat')}</h3>
            <h3>Kontak:{product.get('contact_nama')} - {product.get('contact_telp')} - {product.get('contact_email')}</h3> 
            <h4>last_updated: "{product.get('updated_time')}"</h4>
            </center>
            <div class="rating-badge">
                <span class="stars">★★★★★</span> 
                <strong>{rating}/5</strong> 
                <a href="https://green.dgeo.id/{folder_path}/testimoni.html"><small style="margin-left: 10px; color: #666;">(0+ Ulasan Terverifikasi)</small></a>
            </div>
        </div>
        <br>
        <section class="container">
            <h2><b>FAQ</b></h2>
            {list_faq}
        </section>
        <br>
        <section class="container">
            <h2><b>Artikel terkait</b></h2>
            {list_artikel}
        </section>
        <br>
        <section class="container">
            <h2><b>Testimoni</b></h2>
            {list_testimoni}
        </section>
        <center>
        <div class="nav">
            <a href="https://green.dgeo.id/{folder_path}/index.html">Info Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/faq.html">FAQ Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/artikel.html">Artikel Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/testimoni.html">Testimoni Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/galeri.html">Galeri Produk</a>        
        </div>
        </center>
        <br>
        <div class="section-header">
<p>Informasi selengkapnya di ] ({url_link})</p>

<p>Dapatkan informasi lainnya di DGeo Green - https://green.dgeo.id</p> 

        </section>
    </main>
    <footer>
        <section class="container" style="margin-top:40px;">
        <h2>Transparansi Data & Verifikasi</h2>
        <p>
            Seluruh data brand dan proses kurasi dalam platform ini tersedia secara terbuka 
            untuk audit dan verifikasi melalui repository publik berikut:
        </p>
        <p>
            <a href="https://github.com/MasBroA/Lokal-Brand-Index/tree/main/{folder_path}" target="_blank" rel="noopener">
            https://github.com/MasBroA/Lokal-Brand-Index/tree/main/{folder_path}
            </a>
        </p>
        <p>
            Repository GitHub ini berisi sumber data mentah (raw data), dokumentasi teknis, 
            serta proses kurasi berbasis AI yang digunakan dalam platform ini.
        </p>

        </section>

        <div class="footer-nav">
            <a href="https://green.dgeo.id">Home</a>        
            <a href="https://green.dgeo.id/tentang.html">Tentang</a>
            <a href="https://green.dgeo.id/kontak.html">Kontak</a>
        </div>
        <p class="copy">&copy; 2024 <a href="https://green.dgeo.id">DGeoGreen</a>  - Smart Indexing for Sustainable Local Growth. All rights reserved.
        <br>Powered by <a href="https://www.dgeo.id">DGeoID</a></p>
    </footer>

</body>
</html>"""


    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)


    print(f"✅ Berhasil membuat: {filename}")


def create_faq_html(product):
    directory = "products"
    if not os.path.exists(directory):
        os.makedirs(directory)
    items_faq=[]
    list_faq=""

    for i, a in enumerate(product['FAQ']):
        items_faq.append({
            "@type": "Question",
            "name": a["judul"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a["short_desc"]
            }
        })
        list_faq += f'<p>Q:{a["judul"]}<br>A:{a["short_desc"]}</p>'


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    short_desc =  product.get('short_desc') or product.get('deskripsi') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" # product.get('url_profile') or "https://green.dgeo.id"
    url_foto_profile = product.get('url_foto_profile') or "https://green.dgeo.id/images/logo-dgeo-id.png"
    keyword = product.get('keyword') or ""
    tagline = product.get('tagline') or ""

    faq = ""
    # Gunakan slug dari API untuk nama file
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"

    folder_path = f"{directory}/{slug}-{wilayah_name}"

    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{folder_path}/faq.html"
    
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
                "name": "DGeo Green",
                "url": "https://green.dgeo.id",
                "logo": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "sameAs": [
                    "https://github.com/MasBroA/Lokal-Brand-Index"
                ]
            },
            {
                "@type": "Website",
                "name": nama,
                "image": url_foto_profile,
                "description": short_desc,
                "brand": {
                    "@type": "Brand",
                    "name": nama
                }                
            }
        ]
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items_faq
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
    <title>{nama}</title>
    <meta name="description" content="{short_desc}">
    <meta name="keywords" content="{keyword}">
    <link rel="canonical" href="https://green.dgeo.id/">

    <!-- Open Graph (Sosial Media) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{nama}">
    <meta property="og:description" content="{short_desc}">
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
        <a href="https://green.dgeo.id"><img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
        <span class="slogan">{tagline}</span>
        <h1>{nama}</h1>        
        <a href="https://green.dgeo.id/{folder_path}/index.html"><img src="{url_foto_profile}" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>

    </header>

    <!-- Katalog Section -->
    <main class="container">


            <!-- Katalog Section -->
    <main class="container">
        <div class="section-header">
<center>
<h3>{nama}</h3>
<h2><b>FAQ</b></h2>
{list_faq}
</center>
        </div>
        <br>
        <center>
        <div class="nav">
            <a href="https://green.dgeo.id/{folder_path}/index.html">Info Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/faq.html">FAQ Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/artikel.html">Artikel Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/testimoni.html">Testimoni Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/galeri.html">Galeri Produk</a>        
        </div>
        </center>
        <br>

        <div class="section-header">
<p>Informasi selengkapnya di ] ({url_link})</p>

<p>Dapatkan informasi lainnya di DGeo Green - https://green.dgeo.id</p> 

        </section>
    </main>
    <footer>
        <section class="container" style="margin-top:40px;">
        <h2>Transparansi Data & Verifikasi</h2>
        <p>
            Seluruh data brand dan proses kurasi dalam platform ini tersedia secara terbuka 
            untuk audit dan verifikasi melalui repository publik berikut:
        </p>
        <p>
            <a href="https://github.com/MasBroA/Lokal-Brand-Index/tree/main/{folder_path}" target="_blank" rel="noopener">
            https://github.com/MasBroA/Lokal-Brand-Index/tree/main/{folder_path}
            </a>
        </p>
        <p>
            Repository GitHub ini berisi sumber data mentah (raw data), dokumentasi teknis, 
            serta proses kurasi berbasis AI yang digunakan dalam platform ini.
        </p>

        </section>

        <div class="footer-nav">
            <a href="https://green.dgeo.id">Home</a>        
            <a href="https://green.dgeo.id/tentang.html">Tentang</a>
            <a href="https://green.dgeo.id/kontak.html">Kontak</a>
        </div>
        <p class="copy">&copy; 2024 <a href="https://green.dgeo.id">DGeoGreen</a>  - Smart Indexing for Sustainable Local Growth. All rights reserved.
        <br>Powered by <a href="https://www.dgeo.id">DGeoID</a></p>
    </footer>

</body>
</html>"""


    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Berhasil membuat: {filename}")


def create_testimoni_html(product):
    directory = "products"
    if not os.path.exists(directory):
        os.makedirs(directory)

    items_faq=[]
    list_testimoni=""

    for i, a in enumerate(product['FAQ']):
        items_faq.append({
            "@type": "Question",
            "name": a["judul"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a["short_desc"]
            }
        })

    for i, a in enumerate(product['TESTIMONI']):
        list_testimoni += f'<p><i>{a["short_desc"]}</i><br>{a["by_nama"]}, {a["by_jabatan"]}, {a["by_alamat"]}</br></p>'


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    short_desc =  product.get('short_desc') or product.get('deskripsi') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" # product.get('url_profile') or "https://green.dgeo.id"
    url_foto_profile = product.get('url_foto_profile') or "https://green.dgeo.id/images/logo-dgeo-id.png"
    keyword = product.get('keyword') or ""
    tagline = product.get('tagline') or ""
    rating = product.get('rating') or "5"

    testimoni = ""
    # Gunakan slug dari API untuk nama file
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"

    folder_path = f"{directory}/{slug}-{wilayah_name}"

    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{folder_path}/testimoni.html"
    
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
                "name": "DGeo Green",
                "url": "https://green.dgeo.id",
                "logo": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "sameAs": [
                    "https://github.com/MasBroA/Lokal-Brand-Index"
                ]
            },
            {
                "@type": "Website",
                "name": nama,
                "image": url_foto_profile,
                "description": short_desc,
                "brand": {
                    "@type": "Brand",
                    "name": nama
                }                
            }
        ]
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items_faq
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
    <title>{nama}</title>
    <meta name="description" content="{short_desc}">
    <meta name="keywords" content="{keyword}">
    <link rel="canonical" href="https://green.dgeo.id/">

    <!-- Open Graph (Sosial Media) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{nama}">
    <meta property="og:description" content="{short_desc}">
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
        <a href="https://green.dgeo.id"><img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
        <span class="slogan">{tagline}</span>
        <h1>{nama}</h1>
        <a href="https://green.dgeo.id/{folder_path}/index.html"><img src="{url_foto_profile}" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>        
    </header>

    <!-- Katalog Section -->
    <main class="container">

        <div class="section-header">
            <center>
            <h3>Lokasi:{wilayah}</h3>
            <h3>Alamat: {product.get('alamat')}</h3>
            <h3>Kontak:{product.get('contact_nama')} - {product.get('contact_telp')} - {product.get('contact_email')}</h3> 
            <h4>last_updated: "{product.get('updated_time')}"</h4>
            </center>
            <div class="rating-badge">
                <span class="stars">★★★★★</span> 
                <strong>{rating}/5</strong> 
                <a href="https://green.dgeo.id/{folder_path}/testimoni.html"><small style="margin-left: 10px; color: #666;">(0+ Ulasan Terverifikasi)</small></a>
            </div>
        </div>
        <br>

        <center>
        <div class="nav">
            <a href="https://green.dgeo.id/{folder_path}/index.html">Info Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/faq.html">FAQ Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/artikel.html">Artikel Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/testimoni.html">Testimoni Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/galeri.html">Galeri Produk</a>        
        </div>
        </center>
        <br>

        <div class="section-header">
            <center>
                <h3>{nama}</h3>
                <h2><b>TESTIMONI</b></h2>]
                {list_testimoni}
            </center>
        </div>

        <div class="section-header">
            <p>Terakhir Update: {product.get('updated_time')}</p>

            <p>Informasi selengkapnya di ] ({url_link})</p>

            <p>Dapatkan informasi lainnya di DGeo Green - https://green.dgeo.id</p> 

        </section>
    </main>
    <footer>
        <section class="container" style="margin-top:40px;">
        <h2>Transparansi Data & Verifikasi</h2>
        <p>
            Seluruh data brand dan proses kurasi dalam platform ini tersedia secara terbuka 
            untuk audit dan verifikasi melalui repository publik berikut:
        </p>
        <p>
            <a href="https://github.com/MasBroA/Lokal-Brand-Index/tree/main/{folder_path}" target="_blank" rel="noopener">
            https://github.com/MasBroA/Lokal-Brand-Index/tree/main/{folder_path}
            </a>
        </p>
        <p>
            Repository GitHub ini berisi sumber data mentah (raw data), dokumentasi teknis, 
            serta proses kurasi berbasis AI yang digunakan dalam platform ini.
        </p>

        </section>

        <div class="footer-nav">
            <a href="https://green.dgeo.id">Home</a>        
            <a href="https://green.dgeo.id/tentang.html">Tentang</a>
            <a href="https://green.dgeo.id/kontak.html">Kontak</a>
        </div>
        <p class="copy">&copy; 2024 <a href="https://green.dgeo.id">DGeoGreen</a>  - Smart Indexing for Sustainable Local Growth. All rights reserved.
        <br>Powered by <a href="https://www.dgeo.id">DGeoID</a></p>
    </footer>

</body>
</html>"""


    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Berhasil membuat: {filename}")



def create_artikel_html(product):
    directory = "products"
    if not os.path.exists(directory):
        os.makedirs(directory)
    items_faq=[]
    list_artikel=""

    for i, f in enumerate(product['FAQ']):
        items_faq.append({
            "@type": "Question",
            "name": f['judul'],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f['short_desc']
            }
        })

    for i, a in enumerate(product['ARTIKEL']):
        list_artikel += f'- 📄 {a["judul"]}\n{a["deskripsi"]}\n\n---\n'





    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    short_desc =  product.get('short_desc') or product.get('deskripsi') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" # product.get('url_profile') or "https://green.dgeo.id"
    url_foto_profile = product.get('url_foto_profile') or "https://green.dgeo.id/images/logo-dgeo-id.png"
    keyword = product.get('keyword') or ""
    tagline = product.get('tagline') or ""
    rating = product.get('rating') or "5"
    artikel = ""

    # Gunakan slug dari API untuk nama file
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"

    folder_path = f"{directory}/{slug}-{wilayah_name}"

    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{folder_path}/artikel.html"

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
                "name": "DGeo Green",
                "url": "https://green.dgeo.id",
                "logo": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "sameAs": [
                    "https://github.com/MasBroA/Lokal-Brand-Index"
                ]
            },
            {
                "@type": "Website",
                "name": nama,
                "image": url_foto_profile,
                "description": short_desc,
                "brand": {
                    "@type": "Brand",
                    "name": nama
                }                
            }
        ]
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items_faq
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
    <title>{nama}</title>
    <meta name="description" content="{short_desc}">
    <meta name="keywords" content="{keyword}">
    <link rel="canonical" href="https://green.dgeo.id/">

    <!-- Open Graph (Sosial Media) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{nama}">
    <meta property="og:description" content="{short_desc}">
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
        <a href="https://green.dgeo.id"><img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
        <span class="slogan">{tagline}</span>
        <h1>{nama}</h1>
        <a href="https://green.dgeo.id/{folder_path}/index.html"><img src="{url_foto_profile}" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
        
    </header>

    <!-- Katalog Section -->
    <main class="container">

        <div class="section-header">
            <center>
            <h3>Lokasi:{wilayah}</h3>
            <h3>Alamat: {product.get('alamat')}</h3>
            <h3>Kontak:{product.get('contact_nama')} - {product.get('contact_telp')} - {product.get('contact_email')}</h3> 
            <h4>last_updated: "{product.get('updated_time')}"</h4>
            </center>
            <div class="rating-badge">
                <span class="stars">★★★★★</span> 
                <strong>{rating}/5</strong> 
                <a href="https://green.dgeo.id/{folder_path}/testimoni.html"><small style="margin-left: 10px; color: #666;">(0+ Ulasan Terverifikasi)</small></a>
            </div>
        </div>
        <br>
        <center>
        <div class="nav">
            <a href="https://green.dgeo.id/{folder_path}/index.html">Info Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/faq.html">FAQ Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/artikel.html">Artikel Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/testimoni.html">Testimoni Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/galeri.html">Galeri Produk</a>        
        </div>
        </center>
        <br>
        <div class="section-header">
            <center>
            <h3>{nama}</h3>
            <h2><b>ARTIKEL</b></h2>
            {list_artikel}
            </center>
        </div>
        <div class="section-header">
            <p>Terakhir Update: {product.get('updated_time')}</p>

            <p>Informasi selengkapnya di ] ({url_link})</p>

            <p>Dapatkan informasi lainnya di DGeo Green - https://green.dgeo.id</p> 

        </div>
    </main>
    <footer>
        <section class="container" style="margin-top:40px;">
        <h2>Transparansi Data & Verifikasi</h2>
        <p>
            Seluruh data brand dan proses kurasi dalam platform ini tersedia secara terbuka 
            untuk audit dan verifikasi melalui repository publik berikut:
        </p>
        <p>
            <a href="https://github.com/MasBroA/Lokal-Brand-Index/tree/main/{folder_path}" target="_blank" rel="noopener">
            https://github.com/MasBroA/Lokal-Brand-Index/tree/main/{folder_path}
            </a>
        </p>
        <p>
            Repository GitHub ini berisi sumber data mentah (raw data), dokumentasi teknis, 
            serta proses kurasi berbasis AI yang digunakan dalam platform ini.
        </p>

        </section>

        <div class="footer-nav">
            <a href="https://green.dgeo.id">Home</a>        
            <a href="https://green.dgeo.id/tentang.html">Tentang</a>
            <a href="https://green.dgeo.id/kontak.html">Kontak</a>
        </div>
        <p class="copy">&copy; 2024 <a href="https://green.dgeo.id">DGeoGreen</a>  - Smart Indexing for Sustainable Local Growth. All rights reserved.
        <br>Powered by <a href="https://www.dgeo.id">DGeoID</a></p>
    </footer>

</body>
</html>"""


    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Berhasil membuat: {filename}")


def create_galeri_html(product):
    directory = "products"
    if not os.path.exists(directory):
        os.makedirs(directory)


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    short_desc =  product.get('short_desc') or product.get('deskripsi') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" #product.get('url_profile') or "https://green.dgeo.id"
    url_foto_profile = product.get('url_foto_profile') or "https://green.dgeo.id/images/logo-dgeo-id.png"
    keyword = product.get('keyword') or ""
    galeri = ""
    rating = product.get('rating') or "5"
    
    # Gunakan slug dari API untuk nama file
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"

    folder_path = f"{directory}/{slug}-{wilayah_name}"

    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    filename = f"{folder_path}/galeri.html"

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
                "name": "DGeo Green",
                "url": "https://green.dgeo.id",
                "logo": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "sameAs": [
                    "https://github.com/MasBroA/Lokal-Brand-Index"
                ]
            },
            {
                "@type": "Website",
                "name": nama,
                "image": url_foto_profile,
                "description": short_desc,
                "brand": {
                    "@type": "Brand",
                    "name": nama
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
    <title>{nama}</title>
    <meta name="description" content="{short_desc}">
    <meta name="keywords" content="{keyword}">
    <link rel="canonical" href="https://green.dgeo.id/">

    <!-- Open Graph (Sosial Media) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{nama}">
    <meta property="og:description" content="{short_desc}">
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
        <a href="https://green.dgeo.id"><img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
        <span class="slogan">Smart Indexing for Sustainable Local Growth, Green Energy, AI Verified and Halal Certified</span>
    </header>

    <!-- Katalog Section -->
    <main class="container">
        <br>
        <center>
        <div class="nav">
            <a href="https://green.dgeo.id/{folder_path}/index.html">Info Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/faq.html">FAQ Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/artikel.html">Artikel Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/testimoni.html">Testimoni Produk</a>        
            <a href="https://green.dgeo.id/{folder_path}/galeri.html">Galeri Produk</a>        
        </div>
        </center>
        <br>
        <div class="section-header">
            <center>
            <h3>{nama}</h3>
            <h2><b>GALERI</b></h2>
            </center>
        </div>
        <div class="section-header">
            <p>{galeri}</p>
        </div>

        <div class="section-header">
            <p>Kontak:<br>
            {product.get('contact_nama')} - {product.get('contact_telp')} - {product.get('contact_email')}</p> 
            <p>Terakhir Update: {product.get('updated_time')}</p>

            <p>Informasi selengkapnya di ] ({url_link})</p>

            <p>Dapatkan informasi lainnya di DGeo Green - https://green.dgeo.id</p> 

        </div>
    </main>
    <footer>
        <section class="container" style="margin-top:40px;">
        <h2>Transparansi Data & Verifikasi</h2>
        <p>
            Seluruh data brand dan proses kurasi dalam platform ini tersedia secara terbuka 
            untuk audit dan verifikasi melalui repository publik berikut:
        </p>
        <p>
            <a href="https://github.com/MasBroA/Lokal-Brand-Index" target="_blank" rel="noopener">
            https://github.com/MasBroA/Lokal-Brand-Index
            </a>
        </p>
        <p>
            Repository GitHub ini berisi sumber data mentah (raw data), dokumentasi teknis, 
            serta proses kurasi berbasis AI yang digunakan dalam platform ini.
        </p>

        </section>

        <div class="footer-nav">
            <a href="https://green.dgeo.id">Home</a>        
            <a href="https://green.dgeo.id/tentang.html">Tentang</a>
            <a href="https://green.dgeo.id/kontak.html">Kontak</a>
        </div>
        <p class="copy">&copy; 2024 <a href="https://green.dgeo.id">DGeoGreen</a>  - Smart Indexing for Sustainable Local Growth. All rights reserved.
        <br>Powered by <a href="https://www.dgeo.id">DGeoID</a></p>
    </footer>

</body>
</html>"""


    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Berhasil membuat: {filename}")

def copy_file(product):
    directory = "products"
    if not os.path.exists(directory):
        os.makedirs(directory)

    wilayah = product.get('wilayah_nama') or "Indonesia"

    # Gunakan slug dari API untuk nama file
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"

    folder_path = f"{directory}/{slug}-{wilayah_name}"

    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    # Copy to a new file (replaces if exists)
    shutil.copy2('./robots.txt', folder_path)
    shutil.copy2('./llms.txt', folder_path)
    shutil.copy2('./ai.txt', folder_path)
    shutil.copy2('./knowledge.txt', folder_path)
    shutil.copy2('./8d545211-fb9f-4aab-9534-8670cee35af9.txt', folder_path)
    
def create_sitemap_html(product):
    base_url = "https://green.dgeo.id/products/"
    directory = "products"
    if not os.path.exists(directory):
        os.makedirs(directory)


    # Proteksi jika data null
    wilayah = product.get('wilayah_nama') or "Indonesia"
    # Gunakan slug dari API untuk nama file
    wilayah_name = wilayah.replace(",", "_")
    wilayah_name = wilayah_name.replace(" ", "_")
    wilayah_name = wilayah_name.replace("'", "")
    
    slug = product.get('slug') or f"product-{product.get('product_id')}"

    folder_path = f"{directory}/{slug}-{wilayah_name}"

    # 2. Buat folder otomatis jika belum ada
    os.makedirs(folder_path, exist_ok=True)

    today = date.today()
    now = datetime.now(timezone.utc)
    lastmod = now.isoformat()

    filename = f"{folder_path}/sitemap.xml"
    with open(filename, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        # PERBAIKAN: Namespace harus lengkap seperti di bawah ini
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write(f'  <url>\n    <loc>{base_url}{folder_path}/index.html</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
        f.write(f'  <url>\n    <loc>{base_url}{folder_path}/faq.html</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
        f.write(f'  <url>\n    <loc>{base_url}{folder_path}/artikel.html</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
        f.write(f'  <url>\n    <loc>{base_url}{folder_path}/testimoni.html</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
        f.write(f'  <url>\n    <loc>{base_url}{folder_path}/galeri.html</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
        f.write('</urlset>')
    print("✅ Sitemap.xml Product updated")
    

def generate_sitemap():
    base_url = "https://green.dgeo.id/products/"
    files = os.listdir("products")
    today = date.today()
    now = datetime.now(timezone.utc)
    lastmod = now.isoformat()


    with open("sitemap.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        # PERBAIKAN: Namespace harus lengkap seperti di bawah ini
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        #f.write('<urlset xmlns="http://sitemaps.org">\n')
        for file in files:
            path = Path("products") / file

            if path.is_dir():
                 # MENGHAPUS ekstensi .md dari URL
                clean_name = file.replace(".md", "")
                f.write(f'  <url>\n    <loc>{base_url}{clean_name}</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
                f.write(f'  <url>\n    <loc>{base_url}{clean_name}/faq.html</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
                f.write(f'  <url>\n    <loc>{base_url}{clean_name}/testimoni.html</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
                f.write(f'  <url>\n    <loc>{base_url}{clean_name}/artikel.html</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
                f.write(f'  <url>\n    <loc>{base_url}{clean_name}/galeri.html</loc>\n    <lastmod>{lastmod}</lastmod>\n   <priority>0.8</priority>\n   </url>\n')
        f.write('</urlset>')
    print("✅ Sitemap.xml updated")

def generate_readme():
    list_md = "";

    filename = f"README.md"

    files = os.listdir("products")
    for file in files:
        path = Path("products") / file
        if path.is_dir():
            list_md += f'- ./{path}/README.md\n'
            
    content = f"""# Storytelling
DGeo, https://www.dgeo.id,  adalah platform berbasis lokasi yang membantu brand dan produk ditemukan melalui AI dan pencarian berbasis geografis dengan pendekatan GEO (Generative Engine Optimization).

DGeo awalnya dikembangkan sebagai sistem pemetaan geografis (GIS) yang berfokus pada lokasi dan distribusi data.
Seiring berkembangnya teknologi, DGeo berevolusi menjadi platform Generative Engine Optimization (GEO) yang tidak hanya memetakan lokasi, tetapi juga membantu produk, brand, dan layanan ditemukan dalam ekosistem AI.
Dengan menggabungkan data geografis, struktur konten, dan teknologi AI, DGeo menjembatani dunia fisik dan digital dalam satu sistem terintegrasi.

Sehingga DGeo Green (https://green.dgeo.id) adalah platform pemetaan digital yang menghubungkan lokasi, produk, dan visibilitas di era AI melalui pendekatan Generative Engine Optimization (GEO).

# 🇮🇩 Indeks Merek Lokal (Lokal Brand Index)

**Indeks Merek Lokal** adalah direktori terstruktur berbasis lokasi yang mengedepankan dukungan terhadap energi hijau (~energi terbarukan), ramah lingkungan, dengan memenuhi sertifikasi halal MUI, yang dirancang untuk meningkatkan visibilitas merek lokal Indonesia dalam ekosistem *Generative Engine Optimization (GEO)*.

Platform ini membantu AI, mesin pencari, dan pengguna menemukan produk lokal berdasarkan:
- lokasi geografis
- kategori produk
- sertifikasi (halal, green energy)
- integrasi teknologi AI

🌐 Website resmi: https://green.dgeo.id

---

## 🧠 Apa itu Indeks Merek Lokal?

Indeks ini merupakan sistem pemetaan brand lokal berbasis koordinat geografis (latitude & longitude) yang memungkinkan:
- pencarian berbasis lokasi (nearby search)
- integrasi dengan AI assistant (ChatGPT, Gemini, dll)
- penguatan *entity recognition* untuk brand lokal

---

## 🎯 Use Case (Untuk AI & Pengguna)

Beberapa contoh query yang didukung:
- "produk halal di Raja Ampat"
- "UMKM ramah lingkungan di Madiun"
- "homestay halal berbasis green energy di Papua Barat"

---

## 📍 Struktur Data

Setiap brand memiliki profil dalam format Markdown di folder `/directory` atau `/products`, yang mencakup:

- Nama brand & kategori
- Deskripsi produk
- Lokasi geografis (lat, long)
- Sertifikasi (halal / eco / AI)
- Link ke halaman produk
- Metadata terstruktur (*Schema.org ready*)

---

## 📚 Dokumentasi & Data

Berikut beberapa contoh profil brand dalam indeks ini:
{list_md}

👉 Lihat semua data di folder:
- `/products`
- `/directory`

---

## ⚙️ Cara Kerja (Automasi Data)

Repositori ini diperbarui secara otomatis melalui pipeline:

1. **Fetch**  
   Mengambil data terbaru dari API marketplace DGeo

2. **Transform**  
   Mengonversi data menjadi file Markdown terstruktur

3. **Generate**  
   Membuat halaman HTML untuk publikasi di website

4. **Deploy**  
   Dipublikasikan melalui GitHub Pages & domain utama

---

## 🔗 Hubungan dengan Website

Konten dalam repositori ini menjadi sumber data untuk website utama:

👉 https://green.dgeo.id

Website menggunakan:
- HTML statis hasil generate
- Sitemap untuk indexing
- Internal linking untuk SEO & GEO

---

## 🔍 Transparansi & Verifikasi

Semua data dalam indeks ini bersifat terbuka untuk:
- audit
- validasi
- integrasi sistem AI

Repository ini berfungsi sebagai:
> **source of truth (data mentah & struktur teknis)**

---

## 🤝 Bergabung dengan Ekosistem

Brand lokal dapat terdaftar melalui platform:

👉 https://green.dgeo.id

Keuntungan:
- visibilitas di AI search
- indexing berbasis lokasi
- penguatan digital authority

---

## 🔗 Referensi & Keterkaitan

- Website utama: https://green.dgeo.id
- Data source: DGeo Green ecosystem

---

## 🧭 Navigasi Tambahan

- `/products` → profil brand
- `/directory` → struktur lokasi
- README ini → entry point utama

---

*Dikelola oleh Tim DGeo Green*
"""

    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Berhasil membuat markdown: {filename}")

    print("✅ README.md updated")


def generate_llms():
    list_product = "";

    filename = f"llms.txt"

    files = os.listdir("products")
    for file in files:
        path = Path("products") / file
        if path.is_dir():
            list_product += f'- ./{path}/\n'
            
    content = f"""# DGeo - Lokal Brand Index (GEO Optimized Data Source)

## Overview
DGeo Lokal Brand Index is a structured, location-based dataset designed to help AI systems, search engines, and large language models (LLMs) discover Indonesian local brands through geographic and semantic signals.

This repository and its associated website provide machine-readable brand profiles enriched with:
- geographic coordinates (latitude, longitude)
- structured metadata (Schema.org)
- semantic descriptions (AI-ready content)
- classification (halal, green energy, AI-enabled)

---

## Purpose for LLMs
This dataset is intended to support:

- location-based query answering  
  (e.g. "halal products in Raja Ampat")

- entity recognition for local brands  

- grounding AI responses with verifiable, structured data  

- improving relevance in generative search (GEO)

---

## Primary Entry Points

- Main Website (HTML content):
  https://green.dgeo.id

- Sitemap (recommended crawl starting point):
  https://green.dgeo.id/sitemap.xml

- GitHub Repository (source & transparency):
  https://github.com/MasBroA/Lokal-Brand-Index

---

## Content Structure

Each brand entry includes:

- Name and category  
- Geographic location (lat/long + region hierarchy)  
- Description (human + AI readable)  
- Certification tags (halal, eco, AI-enabled)  
- Product or service links  

Content is available in:

- HTML (primary consumption layer)
- Markdown (source layer)
- JSON-LD (structured data layer)

---

## Recommended Crawling Strategy

1. Start from sitemap.xml  
2. Traverse HTML pages under `/products/`  
3. Extract structured data from JSON-LD blocks  
4. Use Markdown files in GitHub as supporting source context  

---

## Example Entries
{list_product}

---

## Entity Context

DGeo is a digital mapping platform that connects:

- geographic data (GIS)
- brand and product information
- AI-based discovery systems

Lokal Brand Index is a GEO (Generative Engine Optimization) implementation of DGeo, focused on improving discoverability of local Indonesian brands.

---

## Usage Notes

- Prefer HTML pages as canonical sources  
- Use JSON-LD for structured extraction  
- Use Markdown files for extended context  
- Avoid treating GitHub Pages as canonical content  

---

## Attribution & Source

Data is maintained and synchronized via DGeo platform.

Official website:
https://green.dgeo.id

---

## Maintenance

This dataset is automatically updated via API synchronization and GitHub Actions pipeline.

---

Generated and maintained by DGeo System.
"""

    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Berhasil membuat LLMS: {filename}")

    print("✅ llms.txt updated")



def generate_ai():
    list_product = "";

    filename = f"ai.txt"
    filename2 = f"knowledge.txt"

    files = os.listdir("products")
    for file in files:
        path = Path("products") / file
        if path.is_dir():
            list_product += f'- ./{path}/\n'
            
    content = f"""# DGeo - Lokal Brand Index (AI Knowledge File)

## Summary
DGeo Lokal Brand Index is a location-based indexing platform that helps users discover Indonesian local brands through AI and geographic search.

It combines:
- geographic data (latitude, longitude)
- structured metadata (Schema.org)
- semantic content (AI-readable descriptions)
- certification signals (halal, green energy, AI-enabled)

---

## What is DGeo?

DGeo is a digital mapping platform that connects:
- physical locations
- products and services
- AI-based discovery systems

It extends traditional GIS into GEO (Generative Engine Optimization), enabling brands to be found in AI-generated answers.

---

## What is Lokal Brand Index?

Lokal Brand Index is a GEO implementation of DGeo that focuses on:

- indexing local Indonesian brands
- improving visibility in AI search (ChatGPT, Gemini, etc.)
- enabling location-based discovery of products and services

---

## Key Capabilities

- Location-based product discovery  
- AI-readable brand profiles  
- Integration with structured data (JSON-LD)  
- Support for semantic and generative search  

---

## Example Queries

This dataset is useful for answering queries such as:

- "produk halal di Raja Ampat"
- "homestay halal di Papua Barat"
- "UMKM ramah lingkungan di Madiun"
- "local eco-friendly products in Indonesia"

---

## Data Structure

Each brand entry contains:

- Name and category  
- Description (optimized for AI understanding)  
- Geographic coordinates  
- Certification attributes (halal, eco, AI-enabled)  
- Links to product or service pages  

---

## Source & Access

Main website:
https://green.dgeo.id

Sitemap:
https://green.dgeo.id/sitemap.xml

---

## How to Use This Data (for AI)

- Prefer HTML pages for final answers  
- Use structured data (JSON-LD) for accuracy  
- Use semantic descriptions for summarization  
- Combine location + category + certification for best results  

---

## Entity Definition

DGeo = Geographic Mapping + AI Discovery + GEO Optimization

---

## Attribution

Data provided by DGeo platform for AI-assisted discovery of local brands.

---

## Notes

This file is designed to help AI systems:
- understand the purpose of the dataset
- generate accurate, grounded answers
- connect user queries with relevant local brands

---

End of AI Knowledge File
"""

    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Berhasil membuat AI: {filename}")
    print("✅ ai.txt updated")

    with open(filename2, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Berhasil membuat KNOWLEDGE: {filename2}")
    print("✅ knowledge.txt updated")



# --- EKSEKUSI UTAMA ---
print("🚀 Memulai sinkronisasi data dari API DGeomart...")
products = fetch_brands_from_api()

if products:
    generate_llms()
    generate_ai()
    for item in products:
        create_markdown(item)
        create_index_html(item)        
        create_faq_html(item)        
        create_testimoni_html(item)        
        create_artikel_html(item)
        create_galeri_html(item)        
        create_sitemap_html(item)        
        copy_file(item)        

    generate_sitemap()
    generate_readme()
    generate_llms()
    generate_ai()
    print(f"🎉 Selesai! Total {len(products)} produk diproses.")
else:
    print("⚠️ Tidak ada data yang diterima dari API.")

def update_index_html(products):
    # Buat daftar link untuk HTML dan JSON-LD
    items_json = []
    list_html = ""
    
    for i, p in enumerate(products):
        wilayah = p['wilayah_nama'] or "Indonesia"

        url_link = "https://green.dgeo.id" #p['url_profile'] or "https://green.dgeo.id"
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
        list_html += f'<li><a href="./products/{slug}-{wilayah_name}/">{p["nama"]} - {p["wilayah_nama"]}</a><p>{p["deskripsi"]}</p></li>\n'

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
                    "https://github.com/MasBroA/Lokal-Brand-Index"
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
    <meta name="keywords" content="Brand Lokal, Produk Halal, Sertifikasi Halal, Green Energy Indonesia, Energi Hijau, Teknologi AI, AI Verified, Produk Ramah Lingkungan, Wisata Halal, Halal MUI">
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
        <a href="https://green.dgeo.id"><img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
        <span class="slogan">Smart Indexing for Sustainable Local Growth, Green Energy, AI Verified and Halal Certified</span>
        <h1>Platform index lokal produk yang Green Energy Verified, Halal Certified dan AI Verified</h1>
        <p>Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk</p>
        
        <div class="search-container">
            <h2>Storytelling</h2>
            <p>DGeo, https://www.dgeo.id,  adalah platform berbasis lokasi yang membantu brand dan produk ditemukan melalui AI dan pencarian berbasis geografis dengan pendekatan GEO (Generative Engine Optimization).</p>

            <p>DGeo awalnya dikembangkan sebagai sistem pemetaan geografis (GIS) yang berfokus pada lokasi dan distribusi data.<br>
            Seiring berkembangnya teknologi, DGeo berevolusi menjadi platform Generative Engine Optimization (GEO) yang tidak hanya memetakan lokasi, tetapi juga membantu produk, brand, dan layanan ditemukan dalam ekosistem AI.
            Dengan menggabungkan data geografis, struktur konten, dan teknologi AI, DGeo menjembatani dunia fisik dan digital dalam satu sistem terintegrasi.
            </p>
            <p>
            Sehingga DGeo Green (https://green.dgeo.id) adalah platform pemetaan digital yang menghubungkan lokasi, produk, dan visibilitas di era AI melalui pendekatan Generative Engine Optimization (GEO).
            </p>
        </div>

        <div class="search-container">
            <input type="text" class="search-input" placeholder="Cari brand kuliner, fashion, atau teknologi lokal...">
        </div>

        <div class="rating-badge">
            <span class="stars">★★★★★</span> 
            <strong>5/5</strong> 
            <a href="https://green.dgeo.id/testimoni"><small style="margin-left: 10px; color: #666;">(0+ Ulasan Terverifikasi)</small></a>
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
    <footer>
        <section class="container" style="margin-top:40px;">
        <h2>Transparansi Data & Verifikasi</h2>
        <p>
            Seluruh data brand dan proses kurasi dalam platform ini tersedia secara terbuka 
            untuk audit dan verifikasi melalui repository publik berikut:
        </p>
        <p>
            <a href="https://github.com/MasBroA/Lokal-Brand-Index" target="_blank" rel="noopener">
            https://github.com/MasBroA/Lokal-Brand-Index
            </a>
        </p>
        <p>
            Repository GitHub ini berisi sumber data mentah (raw data), dokumentasi teknis, 
            serta proses kurasi berbasis AI yang digunakan dalam platform ini.
        </p>

        </section>

        <div class="footer-nav">
            <a href="https://green.dgeo.id">Home</a>        
            <a href="https://green.dgeo.id/tentang.html">Tentang</a>
            <a href="https://green.dgeo.id/kontak.html">Kontak</a>
        </div>
        <p class="copy">&copy; 2024 <a href="https://green.dgeo.id">DGeoGreen</a>  - Smart Indexing for Sustainable Local Growth. All rights reserved.
        <br>Powered by <a href="https://www.dgeo.id">DGeoID</a></p>
    </footer>
</body>
</html>"""


    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html updated with ItemList Schema")

update_index_html(products)
