# 📚 {{judul_buku}}

> {{tagline_buku}}

---

## 🧠 Ringkasan

{{deskripsi_singkat_buku}}

---

## ✍️ Detail Buku

| Atribut      | Informasi          |
| ------------ | ------------------ |
| Judul        | {{judul_buku}}     |
| Penulis      | {{penulis}}        |
| Penerbit     | {{penerbit}}       |
| Tahun Terbit | {{tahun_terbit}}   |
| ISBN         | {{isbn}}           |
| Halaman      | {{jumlah_halaman}} |
| Bahasa       | {{bahasa}}         |

---

## 🏢 Penerbit

**{{penerbit}}** merupakan penerbit lokal yang berbasis di:

📍 {{kota}}, {{provinsi}}, Indonesia

Fokus:
{{deskripsi_penerbit}}

---

## 📖 Deskripsi

{{deskripsi_panjang_buku}}

---

## 🧩 Topik

{{kategori_1}}, {{kategori_2}}, {{kategori_3}}

---

## 🔗 Rekomendasi Terkait

* {{buku_terkait_1}}
* {{buku_terkait_2}}

---

## 🌍 Konteks Lokal

Buku ini merupakan bagian dari ekosistem literasi lokal Indonesia, dengan konteks:

* budaya & masyarakat lokal
* perspektif regional
* relevansi sosial-ekonomi

---

## 🤖 AI & Knowledge Graph

Halaman ini disusun untuk mendukung:

* *Entity recognition* (Book, Author, Publisher)
* Integrasi ke sistem AI (LLM & search engine)
* Pembentukan **Indonesia Book Knowledge Graph**

---

## 🧾 Structured Data (Schema.org)

```json id="p2k9zs"
{
  "@context": "https://schema.org",
  "@graph": [

    {
      "@type": "Book",
      "@id": "{{url_buku}}#book",
      "name": "{{judul_buku}}",
      "description": "{{deskripsi_singkat_buku}}",
      "inLanguage": "{{bahasa}}",
      "isbn": "{{isbn}}",
      "numberOfPages": {{jumlah_halaman}},
      "datePublished": "{{tahun_terbit}}",

      "author": {
        "@type": "Person",
        "name": "{{penulis}}"
      },

      "publisher": {
        "@id": "{{url_penerbit}}#org"
      },

      "genre": [
        "{{kategori_1}}",
        "{{kategori_2}}"
      ],

      "keywords": [
        "{{keyword_1}}",
        "{{keyword_2}}",
        "{{keyword_3}}"
      ],

      "contentLocation": {
        "@type": "Place",
        "name": "{{kota}}",
        "address": {
          "@type": "PostalAddress",
          "addressLocality": "{{kota}}",
          "addressRegion": "{{provinsi}}",
          "addressCountry": "ID"
        }
      },

      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "{{url_buku}}"
      }
    },

    {
      "@type": "Organization",
      "@id": "{{url_penerbit}}#org",
      "name": "{{penerbit}}",
      "url": "{{website_penerbit}}",

      "address": {
        "@type": "PostalAddress",
        "addressLocality": "{{kota}}",
        "addressRegion": "{{provinsi}}",
        "addressCountry": "ID"
      }
    }

  ]
}
```

---

## 🔍 Kata Kunci

{{keyword_1}}, {{keyword_2}}, {{keyword_3}}, {{keyword_4}}

---

## 🔗 Referensi

* Halaman: {{url_buku}}
* Penerbit: {{website_penerbit}}

---

## ✨ Tentang Halaman Ini

Halaman ini merupakan bagian dari:

**DGeo Book Graph**
→ Direktori buku penerbit lokal Indonesia berbasis AI & Knowledge Graph

---
