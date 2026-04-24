# 📚 {nama}

> {product.get('tagline')}

---

## 🧠 Ringkasan

{product.get('deskripsi')}

{product.get('note')}
---

## ✍️ Detail Buku

| Atribut      | Informasi          |
| ------------ | ------------------ |
| Judul        | {product.get('nama')}     |
| Penulis      | {product.get('contact_nama')}        |
| Penerbit     | {product.get('produsen_nama')}       |
| Tahun Terbit | {product.get('mulai')}   |
| ISBN         | {product.get('kode')}           |
| Halaman      | {product.get('qty')} |
| Bahasa       | {product.get('unit')}         |

---

## 🏢 Penerbit

**{product.get('produsen_nama')}** merupakan penerbit lokal yang berbasis di:

📍 {product.get('produsen_alamat')}

- Telepon: {product.get('produsen_telp')}
- Email: {product.get('produsen_email')}

last_updated: "{product.get('updated_time')}"

---

## 🔗 Link Terkait

- 🌐 Logo Produk/Brand:
  ({url_foto_profile})

- 🌐 Website resmi:
  ({url_link})

- 📄 Halaman produk:
  https://book.dgeo.id/{directory}/{slug}-{wilayah_name}/

---

## 🧩 Topik

{product.get('kategori')}

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

{json_ld}

---

## 🔍 Kata Kunci

{product.get('keyword')}

---


## ✨ Tentang Halaman Ini

Halaman ini merupakan bagian dari:

**DGeo Book Graph**
→ Direktori buku penerbit lokal Indonesia berbasis AI & Knowledge Graph

---

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
  https://book.dgeo.id

---

## 🔍 Transparansi & Sumber Data
Data dalam halaman ini merupakan bagian dari sistem indeks brand lokal berbasis lokasi yang dikelola oleh DGeo Book.

---

## 🧭 Lihat juga
- [Indeks utama](/README.md)
