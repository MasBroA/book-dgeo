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


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" #product.get('url_profile') or "https://green.dgeo.id"
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

[Dapatkan informasi lainnya di] DGeo Green - https://green.dgeo.id/{directory}/{slug}-{wilayah_name}/ 

"""

    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Berhasil membuat markdown: {filename}")

def create_index_html(product):
    directory = "products"
    if not os.path.exists(directory):
        os.makedirs(directory)


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" # product.get('url_profile') or "https://green.dgeo.id"
    keyword = product.get('keyword') or ""

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
                "name": "Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified",
                "image": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "description": "Platform indeks brand lokal terpercaya untuk Sustainable Local Growth...",
                "brand": {
                    "@type": "Brand",
                    "name": "Dgeo Green"
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
    <meta name="keywords" content="{keyword}">
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
        <a href="https://green.dgeo.id"><img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
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
        <div class="rating-badge">
            <span class="stars">★★★★★</span> 
            <strong>4.9/5</strong> 
            <a href="https://green.dgeo.id/testimoni"><small style="margin-left: 10px; color: #666;">(1.250+ Ulasan Terverifikasi)</small></a>
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
<p>{deskripsi}</p>

<p>{catatan}</p>
        </div>

        <div class="section-header">
<p>Kontak:<br>
{product.get('contact_nama')} - {product.get('contact_telp')} - {product.get('contact_email')}</p> 
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
        <p class="copy">&copy; 2024 DGeoGreen  - Smart Indexing for Sustainable Local Growth. All rights reserved.</p>
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


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" #product.get('url_profile') or "https://green.dgeo.id"
    keyword = product.get('keyword') or ""
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
                "name": "Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified",
                "image": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "description": "Platform indeks brand lokal terpercaya untuk Sustainable Local Growth...",
                "brand": {
                    "@type": "Brand",
                    "name": "Dgeo Green"
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
    <meta name="keywords" content="{keyword}">
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
        <a href="https://green.dgeo.id"><img src="https://green.dgeo.id/images/logo-dgeo-id.png" alt="Logo DGeomart Platform Lokal Brand Index Indonesia" loading="lazy" class="logo"></a>
        <span class="slogan">Smart Indexing for Sustainable Local Growth, Green Energy, AI Verified and Halal Certified</span>
    </header>

    <!-- Katalog Section -->
    <main class="container">
        <div class="section-header">
<center>
<h3>{nama}</h3>
<h2><b>FAQ</b></h2>
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
<p>{faq}</p>


        </div>

        <div class="section-header">
<p>Kontak:<br>
{product.get('contact_nama')} - {product.get('contact_telp')} - {product.get('contact_email')}</p> 
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
        <p class="copy">&copy; 2024 DGeoGreen  - Smart Indexing for Sustainable Local Growth. All rights reserved.</p>
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


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" #product.get('url_profile') or "https://green.dgeo.id"
    keyword = product.get('keyword') or ""
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
                "name": "Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified",
                "image": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "description": "Platform indeks brand lokal terpercaya untuk Sustainable Local Growth...",
                "brand": {
                    "@type": "Brand",
                    "name": "Dgeo Green"
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
    <meta name="keywords" content="{keyword}">
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
                <h2><b>TESTIMONI</b></h2>
            </center>
        </div>
        <div class="section-header">
            <p>{testimoni}</p>


        </div>

        <div class="section-header">
            <p>Kontak:<br>
            {product.get('contact_nama')} - {product.get('contact_telp')} - {product.get('contact_email')}</p> 
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
        <p class="copy">&copy; 2024 DGeoGreen  - Smart Indexing for Sustainable Local Growth. All rights reserved.</p>
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


    # Proteksi jika data null
    nama = product.get('nama') or "Produk Tanpa Nama"
    deskripsi = product.get('deskripsi') or product.get('short_desc') or "Deskripsi tidak tersedia."
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" #product.get('url_profile') or "https://green.dgeo.id"
    keyword = product.get('keyword') or ""
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
                "name": "Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified",
                "image": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "description": "Platform indeks brand lokal terpercaya untuk Sustainable Local Growth...",
                "brand": {
                    "@type": "Brand",
                    "name": "Dgeo Green"
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
    <meta name="keywords" content="{keyword}">
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
            <h2><b>ARTIKEL</b></h2>
            </center>
        </div>
        <div class="section-header">
            <p>{artikel}</p>


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
        <p class="copy">&copy; 2024 DGeoGreen  - Smart Indexing for Sustainable Local Growth. All rights reserved.</p>
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
    catatan = product.get('note') or ""
    wilayah = product.get('wilayah_nama') or "Indonesia"
    url_link = "https://green.dgeo.id" #product.get('url_profile') or "https://green.dgeo.id"
    keyword = product.get('keyword') or ""
    galeri = ""
    
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
                "name": "Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified",
                "image": "https://green.dgeo.id/images/logo-dgeo-id.png",
                "description": "Platform indeks brand lokal terpercaya untuk Sustainable Local Growth...",
                "brand": {
                    "@type": "Brand",
                    "name": "Dgeo Green"
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
    <meta name="keywords" content="{keyword}">
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
        <p class="copy">&copy; 2024 DGeoGreen  - Smart Indexing for Sustainable Local Growth. All rights reserved.</p>
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
            list_md += f'- ./products/{path}/README.md\n'
            
    content = f"""# 🇮🇩 Indeks Merek Lokal - Pengoptimal GEO oleh DGeo Green

**Indeks Merek Lokal** adalah direktori berbasis lokasi terstruktur yang dirancang untuk meningkatkan visibilitas merek lokal Indonesia di era *Generative Engine Optimization* (GEO).

Proyek ini memetakan produk dan merek berdasarkan titik koordinat geografis untuk memudahkan AI dan mesin pencari menghubungkan konsumen dengan produsen lokal terdekat.

## 🚀 Misi Kami
Membantu merek lokal "ditemukan" lebih mudah saat pengguna mencari produk spesifik di wilayah tertentu melalui asisten AI (seperti ChatGPT, Gemini) atau pencarian berbasis peta.

## 📍 Struktur Data GEO
Setiap merek dalam indeks ini memiliki profil Markdown khusus di folder `/directory` yang mencakup:
- **Nama Merek & Kategori Produk**
- **Koordinat Geografis (Lat/Long)**
- **Verifikasi Metadata via [DGeo Green](https://green.dgeo.id)**
- **Tautan Langsung ke Etalase Produk**

## 🛠 Cara Kerja (Automasi)
Indeks ini disinkronkan secara otomatis dengan database **DGeo Green** menggunakan GitHub Actions.
1. **Fetch:** Mengambil data merek terbaru dari marketplace.
2. **Transform:** Mengonversi data menjadi file `.md` dengan standar *Schema.org*.
3. **Deploy:** Memperbarui indeks lokasi secara real-time.

## 🤝 Ingin Merek Anda Terdaftar?
Saat ini, indeks ini diprioritaskan bagi merek yang telah tergabung dalam ekosistem **DGeo Green**.
- **Daftar di sini:** [://green.dgeo.id](https://green.dgeo.id)
- **Keuntungan:** Profil merek Anda akan terindeks secara teknis di repositori ini, memperkuat SEO lokal dan otoritas digital produk Anda.

## Lihat juga:
{list_md}

---
*Dikelola oleh [Tim DGeo Green]
*Deployment repo ini ada pada website *https://green.dgeo.id*
"""

    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Berhasil membuat markdown: {filename}")

    print("✅ Sitemap.xml updated")



# --- EKSEKUSI UTAMA ---
print("🚀 Memulai sinkronisasi data dari API DGeomart...")
products = fetch_brands_from_api()

if products:
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
            <input type="text" class="search-input" placeholder="Cari brand kuliner, fashion, atau teknologi lokal...">
        </div>

        <div class="rating-badge">
            <span class="stars">★★★★★</span> 
            <strong>4.9/5</strong> 
            <a href="https://green.dgeo.id/testimoni"><small style="margin-left: 10px; color: #666;">(1.250+ Ulasan Terverifikasi)</small></a>
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
        <p class="copy">&copy; 2024 DGeoGreen  - Smart Indexing for Sustainable Local Growth. All rights reserved.</p>
    </footer>
</body>
</html>"""


    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ index.html updated with ItemList Schema")

update_index_html(products)
