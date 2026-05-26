# 🍽️ FoodGraph — Aplikasi Rekomendasi Makanan Indonesia

Aplikasi rekomendasi makanan berbasis struktur data **Graph** menggunakan algoritma **BFS** dan **DFS**.

## 📁 Struktur Project

```
food-recommendation/
├── app.py                      # Entry point Streamlit (UI utama)
├── requirements.txt            # Dependencies
├── .streamlit/
│   └── config.toml             # Tema dark mode
├── data/
│   └── foods.json              # Dataset 20 makanan + 29 relasi
├── graph/
│   ├── __init__.py
│   └── food_graph.py           # Kelas FoodGraph (Adjacency List + BFS/DFS)
└── components/
    ├── __init__.py
    └── graph_viz.py            # Visualisasi interaktif dengan PyVis
```

## 🧱 Struktur Data

- **Representasi Graf**: Adjacency List (`defaultdict(list)`)
- **Jenis Graf**: Undirected + Weighted (bobot 0.0–1.0)
- **Node**: Setiap makanan (20 node)
- **Edge**: Relasi antar makanan (29 edge)

## ⚙️ Algoritma

### BFS (Breadth-First Search)
- Penelusuran lapis per lapis dari node pilihan
- Menggunakan `deque` sebagai antrian
- Skor = bobot × (1/jarak) → urut dari paling relevan
- Kompleksitas: O(V + E)

### DFS (Depth-First Search)
- Penelusuran rekursif sejauh mungkin dalam satu jalur
- Greedy: prioritas tetangga berbobot tertinggi
- Cocok untuk eksplorasi "keluarga rasa"
- Kompleksitas: O(V + E)

## 🚀 Cara Menjalankan Lokal

```bash
# Clone / download project
cd food-recommendation

# Install dependencies
pip install -r requirements.txt

# Jalankan
streamlit run app.py
```

## 🌐 Deploy ke Streamlit Cloud

1. Upload project ke **GitHub** (repo baru)
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Klik **New app** → pilih repo → set `app.py` sebagai main file
4. Klik **Deploy** — selesai! 🎉

## ✨ Fitur

- 🔍 Rekomendasi berbasis BFS & DFS
- 🕸️ Visualisasi graf interaktif (drag, zoom, hover)
- 🎛️ Filter kategori, tingkat pedas, harga
- 🗺️ Path tracer BFS antar makanan
- 📊 Info kompleksitas algoritma
- 🌙 Desain dark mode premium

## 📚 Mata Kuliah

Struktur Data — Implementasi Graph dengan Python & Streamlit
