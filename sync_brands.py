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
        list_html += f'<li><a href="./directory/{slug}-{wilayah_name}.md">{p["nama"]} - {p["wilayah_nama"]}</a><p>{p["deskripsi"]}</p></li>\n'

    # Gabungkan ke Template
    json_ld_list = json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": items_json
    }, indent=2)

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

    css_content = """
        <style>
        :root { 
            --primary: #1a2a6c; 
            --accent: #27ae60; 
            --gold: #f1c40f; 
            --dark: #111; 
            --wa-green: #25d366; 
            --light-bg: #f0f4f8;
        }
        
        body { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
            margin: 0; 
            color: #333; 
            line-height: 1.6; 
            background-color: #fff;
        }
        
        /* Hero Section */
        .hero { 
            background: linear-gradient(135deg, #ffffff 0%, var(--light-bg) 100%); 
            padding: 80px 20px; 
            text-align: center; 
        }
        .logo { max-width: 160px; margin-bottom: 20px; }
        .slogan { 
            font-size: 0.95rem; 
            color: var(--accent); 
            font-weight: 700; 
            text-transform: uppercase; 
            letter-spacing: 1.5px; 
            display: block; 
            margin-bottom: 10px;
        }
        h1 { font-size: 2.6rem; color: var(--primary); margin: 0 0 20px 0; }
        
        /* AI Search Bar */
        .search-container { max-width: 650px; margin: 30px auto; }
        .search-input { 
            width: 100%; 
            padding: 18px 30px; 
            border-radius: 50px; 
            border: 1px solid #ddd; 
            font-size: 16px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.05); 
            outline: none; 
            transition: 0.3s;
            box-sizing: border-box;
        }
        .search-input:focus { 
            border-color: var(--accent); 
            box-shadow: 0 10px 30px rgba(39, 174, 96, 0.15); 
        }
        
        /* Rating Badge */
        .rating-badge { 
            display: inline-block; 
            background: white; 
            padding: 10px 25px; 
            border-radius: 50px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
            margin-top: 10px; 
        }
        .stars { color: var(--gold); font-size: 1.2rem; }

        /* Brand Grid */
        .container { max-width: 1100px; margin: 60px auto; padding: 0 20px; }
        .section-header { margin-bottom: 40px; text-align: left; }
        .section-header h2 { 
            font-size: 1.8rem; 
            border-left: 6px solid var(--accent); 
            padding-left: 15px; 
            color: var(--primary);
        }
        
        .brand-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); 
            gap: 25px; 
        }
        .brand-card { 
            border: 1px solid #eee; 
            border-radius: 15px; 
            padding: 25px; 
            text-align: center; 
            transition: 0.4s; 
            background: white; 
        }
        .brand-card:hover { 
            transform: translateY(-8px); 
            box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
            border-color: var(--accent); 
        }
        .brand-logo { 
            width: 70px; height: 70px; 
            background: #f8f9fa; 
            border-radius: 50%; 
            margin: 0 auto 15px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 20px; 
            font-weight: bold; 
            color: #cbd5e0; 
        }
        
        .badge { 
            font-size: 10px; 
            padding: 4px 10px; 
            border-radius: 20px; 
            font-weight: 700; 
            margin: 2px; 
            text-transform: uppercase; 
        }
        .badge-halal { background: #dcfce7; color: #166534; }
        .badge-ai { background: #dbeafe; color: #1e40af; }

        /* Call to Action */
        .cta { 
            background: var(--primary); 
            color: white; 
            padding: 80px 20px; 
            text-align: center; 
        }
        .btn-wa { 
            background: var(--wa-green); 
            color: white; 
            padding: 18px 45px; 
            border-radius: 50px; 
            text-decoration: none; 
            font-weight: bold; 
            display: inline-block; 
            font-size: 1.1rem; 
            transition: 0.3s; 
            margin-top: 25px; 
        }
        .btn-wa:hover { 
            background: #1eb956; 
            transform: scale(1.05); 
            box-shadow: 0 10px 20px rgba(37, 211, 102, 0.3); 
        }

        /* Footer */
        footer { background: var(--dark); color: #888; padding: 60px 20px; text-align: center; }
        .footer-nav { margin-bottom: 30px; }
        .footer-nav a { color: #bbb; text-decoration: none; margin: 0 15px; font-size: 14px; transition: 0.3s; }
        .footer-nav a:hover { color: white; }
        .copy { font-size: 12px; color: #555; }
    </style>
    """
    html_content = f"""<!DOCTYPE html>
<!DOCTYPE html>
<html lang="id">
<head>
    <!-- Meta Dasar -->

    <!-- Open Graph (Sosial Media) -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified">
    <meta property="og:description" content="Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk">
    <meta property="og:url" content="https://masbroa.github.io/Lokal-Brand-Index/">

    <!-- Favicon -->
    <link rel="icon" href="https://www.dgeomart.com/ecom/images/logo/logo2.png" type="image/x-icon">

    <meta name="google-site-verification" content="mkts7AhE-ySL6g37ibn9s4Am0HWwEzPyo8cZ2UA_Rdc" />


    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified</title>
    <meta name="description" content="Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk">
    <meta name="keywords" content="Brand Lokal, Sertifikasi Halal, Green Energy Indonesia, Energi Hijau, Teknologi AI, AI Verified, Produk Ramah Lingkungan, Wisata Halal">
    <link rel="canonical" href="https://masbroa.github.io/Lokal-Brand-Index/">

    <!-- JSON-LD Schema: Dioptimalkan untuk Rich Snippets (Bintang Kuning) -->
    <script type="application/ld+json">
    {
        [
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "@id": "https://www.dgeomart.com",
            "name": "DGeomart",
            "url": "https://www.dgeomart.com",
            "logo": "https://www.dgeomart.com/ecom/images/logo/logo2.png",
            "sameAs": [
            "https://instagram.com",
            "https://wa.me"
            ]
        },
        {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "Lokal Brand Index - Smart Indexing for Sustainable Local Growth, Produk Ramah Lingkungan, Halal Certified, and AI Verified",
            "image": "https://www.dgeomart.com/ecom/images/logo/logo2.png",
            "description": "Platform indeks brand lokal terpercaya untuk Sustainable Local Growth dengan standar verifikasi AI, Sertifikasi Halal yang mendukung energi hijau sebagai energi ramah lingkungan dalam setiap proses produksi, penjualan, distribusi termasuk layanan produk",
            "brand": { "@type": "Brand", "name": "DGeomart" },
            "knowsAbout": ["Halal Certification", "Green Energy", "Artificial Intelligence", "Indonesian SMEs"],
                "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "bestRating": "5",
            "worstRating": "1",
            "ratingCount": "1250"
            }
        }
        ]
    }
    </script>
    <!-- 2. SCHEMA FAQ (Memudahkan AI Menjawab Pertanyaan User) -->
    <script type="application/ld+json">
        {json.dumps(faq_schema, indent=2)}
    </script>

    <!-- SKEMA DAFTAR ITEM (Naikkan Skor Discovery) -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "ItemList",
      "itemListElement": {json.dumps(items_json)}
    }}
    </script>

    {css_content}
</head>
<body>
    <!-- Header & Hero -->
    <header class="hero">
        <img src="https://www.dgeomart.com/ecom/images/logo/logo2.png" alt="DGeomart Logo" class="logo">
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
