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
        "desc": "Kain tenun tradisional berkualitas tinggi langsung dari pengrajin.",
        "url": "https://www.dgeomart.com/cbm/product/beras_hitam_marolis"
    }
]

def create_markdown(brand):
    # Folder tujuan
    directory = "directory"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Format isi file Markdown (GEO Friendly)
    content = f"""---
title: "{brand['name']}"
brand_slug: "{brand['slug']}"
category: "{brand['category']}"
geo_location:
  type: "Point"
  coordinates: [{brand['long']}, {brand['lat']}]
address: "{brand['city']}"
source: "{brand['url']}"
---

# {brand['name']} - {brand['city']}

{brand['desc']}

Temukan produk original **{brand['name']}** melalui platform [DGeomart](https://dgeomart.com{brand['slug']}).
"""
    
    # Simpan file
    filename = f"{directory}/{brand['slug']}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Created: {filename}")

# Jalankan proses
for brand in brands_data:
    create_markdown(brand)

