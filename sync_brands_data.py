import os
import json

# Data ini nantinya bisa diganti dengan request.get('https://dgeomart.com')
brands_data = [
    {
        "name": "Keripik Keladi Asin Pelangi Sorong",
        "slug": "keripik-keladi-asin-pelangi-sorong",
        "category": "Makanan Cemilan",
        "lat": -0.8594052,
        "long": 131.2494258,
        "city": "Sorong, Papua Barat",
        "desc": "Bukan sembarang keripik, ini Keripik Keladi Asin Pelangi Sorong. Begitu digigit, aroma nangkanya langsung berasa, teksturnya crunchy dan tidak berminyak.",
        "url": "https://www.dgeomart.com/cbm/product/tld2212160556577993652"
    },
    {
        "name": "Beras Hitam Sehat Marolis Madiun",
        "slug": "beras-hitam-sehat-marolis-madiun",
        "category": "Sembako",
        "lat": -7.6128306,
        "long": 111.40971005,
        "city": "Madiun, Jawa Timur",
        "desc": "Beras organik yang sehat menyehatkan produksi petani di Madiun dengan pupuk organik marolis",
        "url": "https://www.dgeomart.com/cbm/product/beras_hitam_marolis"
    }
]


def create_markdown(brand):
    directory = "directory"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Skema JSON-LD untuk AI
    json_ld = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{brand['name']}",
  "description": "{brand['desc']}",
  "url": "{brand['url']}",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{brand['city']}",
    "addressCountry": "ID"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": {brand['lat']},
    "longitude": {brand['long']}
  }}
}}
</script>
"""

    content = f"""---
title: "{brand['name']} - {brand['city']}"
---
{json_ld}

# {brand['name']} - {brand['city']}
{brand['desc']}

[Cek Produk di DGeomart]({brand['url']})
"""
    # ... (sisanya sama seperti sebelumnya)

    # Simpan file
    filename = f"{directory}/{brand['slug']}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")

# Jalankan proses
for brand in brands_data:
    create_markdown(brand)

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

# Panggil fungsi ini setelah loop brand selesai
generate_sitemap()

