import streamlit as st
import sys
import os

# Path setup
sys.path.insert(0, os.path.dirname(__file__))

from graph.food_graph import FoodGraph
from components.graph_viz import render_graph

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FoodGraph — Rekomendasi Makanan Indonesia",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght=400;700;900&family=DM+Sans:wght=300;400;500;600&display=swap');

/* ── Root & Reset ── */
:root {
    --bg-primary:    #080E1A;
    --bg-secondary:  #0F172A;
    --bg-card:       #111827;
    --bg-card-hover: #1A2538;
    --accent-gold:   #F59E0B;
    --accent-orange: #EA580C;
    --accent-red:    #DC2626;
    --text-primary:  #F8FAFC;
    --text-secondary:#94A3B8;
    --text-muted:    #475569;
    --border:        #1E293B;
    --border-accent: #F59E0B44;
    --glow-gold:     0 0 30px rgba(245,158,11,0.25);
    --radius-sm:     8px;
    --radius-md:     14px;
    --radius-lg:     20px;
}

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stHeader"] {
    background-color: var(--bg-primary) !important;
    border-bottom: 1px solid var(--border) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; }

/* ── Hero Title ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 3.5rem);
    font-weight: 900;
    line-height: 1.1;
    background: linear-gradient(135deg, #F59E0B 0%, #EA580C 50%, #F59E0B 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
    letter-spacing: -0.02em;
    margin: 0;
}

.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    color: var(--text-secondary);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}
.section-header h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}
.section-tag {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent-gold);
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.2);
    padding: 2px 10px;
    border-radius: 999px;
}

/* ── Food Cards ── */
.rec-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    margin-bottom: 0.875rem;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
}
.rec-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #F59E0B, #EA580C);
    opacity: 0;
    transition: opacity 0.25s;
}
.rec-card:hover {
    border-color: var(--border-accent);
    background: var(--bg-card-hover);
    transform: translateX(3px);
    box-shadow: var(--glow-gold);
}
.rec-card:hover::before { opacity: 1; }

.rec-rank {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 900;
    color: var(--text-muted);
    line-height: 1;
}
.rec-rank.top { color: var(--accent-gold); }

.rec-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0.25rem 0;
}
.rec-desc {
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.5;
    margin: 0.25rem 0;
}
.rec-reason {
    font-size: 0.75rem;
    color: var(--accent-gold);
    font-style: italic;
    margin-top: 0.5rem;
    padding-top: 0.5rem;
    border-top: 1px solid var(--border);
}

/* ── Score Bar ── */
.score-bar-container { margin: 0.5rem 0; }
.score-bar-track { background: var(--border); height: 4px; border-radius: 999px; overflow: hidden; }
.score-bar-fill { height: 100%; background: linear-gradient(90deg, #F59E0B, #EA580C); border-radius: 999px; transition: width 1s ease; }
.score-label { font-size: 0.7rem; color: var(--text-muted); margin-bottom: 4px; }

/* ── Tags / Badges ── */
.tag-container { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.5rem 0; }
.tag {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 999px;
    background: rgba(148,163,184,0.08);
    color: var(--text-secondary);
    border: 1px solid var(--border);
}
.tag.pedas    { background: rgba(220,38,38,0.12);  color:#FCA5A5; border-color: rgba(220,38,38,0.25);  }
.tag.gurih    { background: rgba(245,158,11,0.12); color:#FCD34D; border-color: rgba(245,158,11,0.25); }
.tag.manis    { background: rgba(167,139,250,0.12);color:#C4B5FD; border-color: rgba(167,139,250,0.25); }
.tag.sehat    { background: rgba(34,197,94,0.12);  color:#86EFAC; border-color: rgba(34,197,94,0.25);  }
.tag.populer  { background: rgba(251,191,36,0.12); color:#FDE68A; border-color: rgba(251,191,36,0.25); }
.tag.berkuah  { background: rgba(14,165,233,0.12); color:#7DD3FC; border-color: rgba(14,165,233,0.25); }

/* ── Spicy Indicator ── */
.spicy-row { display: flex; align-items: center; gap: 6px; }
.spicy-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--border); }
.spicy-dot.active { background: #EF4444; }

/* ── Stats Cards ── */
.stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 1.2rem 1.5rem; text-align: center; }
.stat-number { font-family: 'Playfair Display', serif; font-size: 2.5rem; font-weight: 900; background: linear-gradient(135deg, #F59E0B, #EA580C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1; }
.stat-label { font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); margin-top: 0.35rem; }

.fancy-divider { border: none; height: 1px; background: linear-gradient(90deg, transparent, var(--border-accent), transparent); margin: 1.5rem 0; }
.empty-state { text-align: center; padding: 3rem 2rem; border: 1px dashed var(--border); border-radius: var(--radius-lg); }
.empty-state-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state-text { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: var(--text-secondary); margin-bottom: 0.5rem; }
.empty-state-hint { font-size: 0.85rem; color: var(--text-muted); }

/* ── Sidebar overrides ── */
[data-testid="stSidebar"] label { color: var(--text-secondary) !important; font-size: 0.85rem !important; font-weight: 500 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; }
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div { background-color: var(--bg-card) !important; border-color: var(--border) !important; color: var(--text-primary) !important; }

/* ── Button styles ── */
.stButton > button {
    background: #111827 !important; color: #94A3B8 !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.82rem !important;
    border: 1.5px solid #1E293B !important; border-radius: 12px !important; padding: 0.9rem 0.5rem !important; transition: all 0.2s ease !important;
    white-space: pre-wrap !important; line-height: 1.5 !important; height: auto !important; min-height: 90px !important; cursor: pointer !important;
}
.stButton > button:hover { border-color: #F59E0B !important; background: #1A2538 !important; color: #F8FAFC !important; transform: translateY(-2px) !important; box-shadow: 0 4px 16px rgba(245,158,11,0.2) !important; }

.btn-action .stButton > button { background: linear-gradient(135deg, #F59E0B, #EA580C) !important; color: #0F0F0F !important; font-weight: 700 !important; font-size: 0.85rem !important; border: none !important; border-radius: var(--radius-sm) !important; padding: 0.65rem 1.5rem !important; min-height: unset !important; height: auto !important; }
.btn-action .stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 20px rgba(245,158,11,0.4) !important; filter: brightness(1.1) !important; }
.btn-reset .stButton > button { background: #1E293B !important; color: #94A3B8 !important; border: 1px solid #334155 !important; font-weight: 600 !important; font-size: 0.85rem !important; border-radius: var(--radius-sm) !important; padding: 0.65rem 1.5rem !important; min-height: unset !important; height: auto !important; }

.path-trace { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; padding: 1rem 1.25rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-md); margin-top: 1rem; }
.path-node { font-size: 0.85rem; font-weight: 600; color: var(--accent-gold); background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.2); padding: 4px 12px; border-radius: 999px; }
.path-arrow { color: var(--text-muted); font-size: 0.9rem; }
.algo-banner { background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(234,88,12,0.08)); border: 1px solid rgba(245,158,11,0.2); border-radius: var(--radius-md); padding: 1rem 1.25rem; margin-bottom: 1.25rem; font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6; }
.algo-banner strong { color: var(--accent-gold); }
</style>
""", unsafe_allow_html=True)


# ─── SAFE BACKING UP FOR GRAPH IN SESSION STATE ───────────────────────────────
if 'graph_instance' not in st.session_state:
    try:
        st.session_state.graph_instance = FoodGraph()
    except Exception as e:
        st.error(f"Gagal menginisialisasi FoodGraph asli: {e}")
        st.stop()

graph = st.session_state.graph_instance

# Pembacaan list makanan yang aman agar filter utama tidak crash
def get_safe_foods_list(g_obj):
    if hasattr(g_obj, 'foods'):
        if isinstance(g_obj.foods, dict):
            return list(g_obj.foods.values())
        elif isinstance(g_obj.foods, list):
            return g_obj.foods
    return []


# ─── SESSION STATE MANAGEMENT ─────────────────────────────────────────────────
if 'selected_foods' not in st.session_state:
    st.session_state.selected_foods = []
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 0 1rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:900;
                    background:linear-gradient(135deg,#F59E0B,#EA580C);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;">
            🍽️ FoodGraph
        </div>
        <div style="font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:#475569;margin-top:4px;">
            Struktur Data — Graph
        </div>
    </div>
    <hr style="border:none;border-top:1px solid #1E293B;margin:0 0 1.5rem;">
    """, unsafe_allow_html=True)

    # Membaca Kategori secara Aman
    try:
        categories = ["Semua"] + [c.title() for c in graph.get_all_categories()]
    except Exception:
        categories = ["Semua", "Makanan Utama", "Cemilan", "Minuman"]
        
    st.markdown("<label>Kategori</label>", unsafe_allow_html=True)
    selected_category = st.selectbox("Kategori", categories, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<label>Maks. Level Pedas</label>", unsafe_allow_html=True)
    max_spicy = st.slider("Pedas", 0, 5, 5, label_visibility="collapsed", format="%d 🌶️")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<label>Kisaran Harga</label>", unsafe_allow_html=True)
    price_opts = ["Semua", "Murah", "Sedang", "Mahal"]
    selected_price = st.selectbox("Harga", price_opts, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<label>Algoritma</label>", unsafe_allow_html=True)
    algo = st.radio("Algoritma", ["BFS (Rekomendasi Cepat)", "DFS (Eksplorasi Mendalam)"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<label>Jumlah Rekomendasi</label>", unsafe_allow_html=True)
    top_n = st.slider("Top N", 3, 12, 6, label_visibility="collapsed")

    st.markdown("""<hr style="border:none;border-top:1px solid #1E293B;margin:1.5rem 0;">""", unsafe_allow_html=True)
    
    # Hitung Statistik Total Node & Edges Secara Aman
    t_nodes, t_edges = 0, 0
    try:
        t_nodes = graph.total_nodes()
        t_edges = graph.total_edges()
    except Exception:
        if hasattr(graph, 'foods'):
            t_nodes = len(graph.foods)
        if hasattr(graph, 'adj_list'):
            t_edges = sum(len(v) for v in graph.adj_list.values()) // 2

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""<div class="stat-card"><div class="stat-number">{t_nodes}</div><div class="stat-label">Makanan</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-card"><div class="stat-number">{t_edges}</div><div class="stat-label">Relasi</div></div>""", unsafe_allow_html=True)

    st.markdown("""<hr style="border:none;border-top:1px solid #1E293B;margin:1.5rem 0;">""", unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # EMULASI CRUD GRAF - ANTI ERROR & DEFENSIF MULTI-STRUKTUR
    # ═══════════════════════════════════════════════════════════════════════════
    with st.expander("🛠️ MANAGE DATA GRAF (CRUD)"):
        crud_mode = st.radio("Aksi Graf", ["Lihat Data (Read)", "Tambah Node (Create)", "Update Node", "Hapus Node (Delete)"])
        
        # Mapping struktur dinamis internal data graf
        foods_map = {}
        if hasattr(graph, 'foods'):
            if isinstance(graph.foods, dict):
                foods_map = graph.foods
            elif isinstance(graph.foods, list):
                for idx, item in enumerate(graph.foods):
                    if isinstance(item, dict):
                        f_id = item.get('id', f"node_{idx}")
                        foods_map[f_id] = item
                    else:
                        f_id = getattr(item, 'id', f"node_{idx}")
                        foods_map[f_id] = item

        # 1. READ ACTION
        if crud_mode == "Lihat Data (Read)":
            st.write("**Daftar Node Graf Saat Ini:**")
            if foods_map:
                for fid, f_data in foods_map.items():
                    if isinstance(f_data, dict):
                        st.text(f"[{fid}] {f_data.get('emoji','🍜')} {f_data.get('name','Tanpa Nama')}")
                    else:
                        st.text(f"[{fid}] {getattr(f_data, 'emoji', '🍜')} {getattr(f_data, 'name', 'Tanpa Nama')}")
            else:
                st.warning("Data graf kosong.")
                
        # 2. CREATE ACTION
        elif crud_mode == "Tambah Node (Create)":
            with st.form("create_node_form"):
                new_id = st.text_input("ID Makanan (lowercase & unik)", placeholder="misal: sate_maranggi")
                new_name = st.text_input("Nama Makanan", placeholder="Sate Maranggi")
                new_emoji = st.text_input("Emoji", value="🍢")
                new_cat = st.text_input("Kategori", value="makanan utama").lower()
                new_price = st.selectbox("Range Harga", ["murah", "sedang", "mahal"])
                new_spicy = st.slider("Level Pedas", 0, 5, 0)
                new_desc = st.text_area("Deskripsi Singkat")
                new_tags = st.text_input("Tags (Pisahkan dengan koma)", placeholder="manis, gurih")
                
                if st.form_submit_button("Simpan Node"):
                    if new_id and new_name:
                        if new_id in foods_map:
                            st.error("ID Makanan tersebut sudah terdaftar!")
                        else:
                            tag_list = [t.strip() for t in new_tags.split(",") if t.strip()]
                            new_node_data = {
                                "id": new_id, "name": new_name, "emoji": new_emoji,
                                "category": new_cat, "price_range": new_price,
                                "spicy_level": new_spicy, "description": new_desc, "tags": tag_list
                            }
                            
                            try:
                                if isinstance(graph.foods, dict):
                                    graph.foods[new_id] = new_node_data
                                elif isinstance(graph.foods, list):
                                    graph.foods.append(new_node_data)
                                
                                # Daftarkan ke relasi struktur adjacency list
                                if hasattr(graph, 'adj_list') and isinstance(graph.adj_list, dict):
                                    if new_id not in graph.adj_list:
                                        graph.adj_list[new_id] = []
                                        
                                st.success(f"Berhasil menyuntikkan node: {new_name}!")
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Gagal menyimpan data ke objek graf: {ex}")
                    else:
                        st.error("ID dan Nama Makanan tidak boleh kosong!")

        # 3. UPDATE ACTION
        elif crud_mode == "Update Node":
            if foods_map:
                target_update_id = st.selectbox("Pilih ID Node", options=list(foods_map.keys()))
                if target_update_id:
                    current_node = foods_map[target_update_id]
                    
                    is_d = isinstance(current_node, dict)
                    c_name = current_node.get('name', '') if is_d else getattr(current_node, 'name', '')
                    c_emoji = current_node.get('emoji', '') if is_d else getattr(current_node, 'emoji', '')
                    c_cat = current_node.get('category', '') if is_d else getattr(current_node, 'category', '')
                    c_price = current_node.get('price_range', 'murah') if is_d else getattr(current_node, 'price_range', 'murah')
                    c_spicy = current_node.get('spicy_level', 0) if is_d else getattr(current_node, 'spicy_level', 0)
                    c_desc = current_node.get('description', '') if is_d else getattr(current_node, 'description', '')
                    c_tags = current_node.get('tags', []) if is_d else getattr(current_node, 'tags', [])

                    with st.form("update_node_form"):
                        up_name = st.text_input("Nama Makanan", value=c_name)
                        up_emoji = st.text_input("Emoji", value=c_emoji)
                        up_cat = st.text_input("Kategori", value=c_cat)
                        up_price = st.selectbox("Harga", ["murah", "sedang", "mahal"], index=["murah", "sedang", "mahal"].index(c_price if c_price in ["murah", "sedang", "mahal"] else "murah"))
                        up_spicy = st.slider("Level Pedas", 0, 5, int(c_spicy))
                        up_desc = st.text_area("Deskripsi", value=c_desc)
                        up_tags = st.text_input("Tags (Koma)", value=", ".join(c_tags) if isinstance(c_tags, list) else "")
                        
                        if st.form_submit_button("Lakukan Perbaruan"):
                            updated_fields = {
                                "name": up_name, "emoji": up_emoji, "category": up_cat.lower(),
                                "price_range": up_price, "spicy_level": up_spicy, "description": up_desc,
                                "tags": [t.strip() for t in up_tags.split(",") if t.strip()]
                            }
                            try:
                                if isinstance(graph.foods, dict):
                                    graph.foods[target_update_id].update(updated_fields)
                                elif isinstance(graph.foods, list):
                                    for idx, item in enumerate(graph.foods):
                                        if isinstance(item, dict) and item.get('id') == target_update_id:
                                            graph.foods[idx].update(updated_fields)
                                        elif not isinstance(item, dict) and getattr(item, 'id', '') == target_update_id:
                                            for k, v in updated_fields.items():
                                                setattr(graph.foods[idx], k, v)
                                st.success("Perubahan data node berhasil disimpan!")
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Gagal melakukan update: {ex}")
            else:
                st.warning("Tidak ada node yang bisa diubah.")

        # 4. DELETE ACTION
        elif crud_mode == "Hapus Node (Delete)":
            if foods_map:
                target_del_id = st.selectbox("Pilih ID Node untuk Dihapus", options=list(foods_map.keys()))
                if st.button("🔴 Eksekusi Hapus", use_container_width=True):
                    try:
                        if isinstance(graph.foods, dict):
                            if target_del_id in graph.foods:
                                del graph.foods[target_del_id]
                        elif isinstance(graph.foods, list):
                            graph.foods = [item for item in graph.foods if (item.get('id') if isinstance(item, dict) else getattr(item, 'id', '')) != target_del_id]
                        
                        # Sinkronisasi pembersihan edges relasi
                        if hasattr(graph, 'adj_list') and isinstance(graph.adj_list, dict):
                            if target_del_id in graph.adj_list:
                                del graph.adj_list[target_del_id]
                            for k, v in graph.adj_list.items():
                                if isinstance(v, list):
                                    graph.adj_list[k] = [edge for edge in v if edge != target_del_id]
                                    
                        if target_del_id in st.session_state.selected_foods:
                            st.session_state.selected_foods.remove(target_del_id)
                            
                        st.success("Node berhasil dihapus secara bersih dari Graf!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Gagal eksekusi hapus: {ex}")
            else:
                st.warning("Tidak ada data yang bisa dihapus.")


# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom: 2rem;">
    <p class="hero-subtitle">Struktur Data · Graph · BFS · DFS</p>
    <h1 class="hero-title">Rekomendasi Makanan<br>Indonesia</h1>
    <p style="color:#64748B;font-size:0.9rem;margin-top:0.75rem;max-width:520px;">
        Temukan hidangan favoritmu berikutnya menggunakan algoritma penelusuran graf.
        Setiap makanan terhubung berdasarkan bahan, rasa, dan kebiasaan makan.
    </p>
</div>
<hr class="fancy-divider">
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🔍  Rekomendasi", "🕸️  Graf Interaktif", "📚  Tentang Algoritma"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: SCREEN REKOMENDASI UTAMA
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:
        cat_filter = None if selected_category == "Semua" else selected_category.lower()
        price_filter = None if selected_price == "Semua" else selected_price.lower()
        
        # Eksekusi filter bawaan secara aman
        try:
            filtered_foods = graph.filter_foods(category=cat_filter, max_spicy=max_spicy, price_range=price_filter)
        except Exception:
            # Fallback jika fungsi .filter_foods() error/tidak kompatibel
            raw_list = get_safe_foods_list(graph)
            filtered_foods = []
            for f in raw_list:
                is_d = isinstance(f, dict)
                f_cat = f.get('category', '') if is_d else getattr(f, 'category', '')
                f_spicy = f.get('spicy_level', 0) if is_d else getattr(f, 'spicy_level', 0)
                f_price = f.get('price_range', '') if is_d else getattr(f, 'price_range', '')
                
                if cat_filter and f_cat.lower() != cat_filter: continue
                if f_spicy > max_spicy: continue
                if price_filter and f_price.lower() != price_filter: continue
                
                filtered_foods.append(f if is_d else f.__dict__)

        st.markdown("""<div class="section-header"><h3>Pilih Makanan Favorit</h3><span class="section-tag">Maks 5</span></div>""", unsafe_allow_html=True)

        if not filtered_foods:
            st.markdown("""<div class="empty-state"><div class="empty-state-icon">🔍</div><div class="empty-state-text">Tidak ada makanan ditemukan</div><div class="empty-state-hint">Coba longgarkan kriteria filter di sidebar</div></div>""", unsafe_allow_html=True)
        else:
            n_cols = 3
            pills_per_row = [filtered_foods[i:i+n_cols] for i in range(0, len(filtered_foods), n_cols)]

            for row in pills_per_row:
                cols = st.columns(len(row))
                for col, food in zip(cols, row):
                    with col:
                        f_id = food.get('id')
                        f_name = food.get('name')
                        f_emoji = food.get('emoji', '🍜')
                        f_spicy = food.get('spicy_level', 0)
                        f_desc = food.get('description', '')

                        is_sel = f_id in st.session_state.selected_foods
                        spicy_str = "🔴" * f_spicy + "⚫" * (5 - f_spicy) if f_spicy > 0 else "⚫⚫⚫⚫⚫"
                        
                        check = "✓ " if is_sel else ""
                        label = f"{f_emoji}\n{check}{f_name}\n{spicy_str}"

                        if is_sel:
                            st.markdown(f"""<style>div[data-testid="stButton"]:has(button[key="pill_{f_id}"]) > button {{ border-color: #F59E0B !important; background: rgba(245,158,11,0.12) !important; color: #F59E0B !important; }}</style>""", unsafe_allow_html=True)

                        if st.button(label, key=f"pill_{f_id}", help=f_desc, use_container_width=True):
                            if f_id in st.session_state.selected_foods:
                                st.session_state.selected_foods.remove(f_id)
                            elif len(st.session_state.selected_foods) < 5:
                                st.session_state.selected_foods.append(f_id)
                            st.rerun()

        # Tampilkan chip pilihan makanan
        if st.session_state.selected_foods:
            st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
            st.markdown("""<div class="section-header"><h3>Makanan Dipilih</h3></div>""", unsafe_allow_html=True)

            sel_chips = []
            for fid in st.session_state.selected_foods:
                if fid in foods_map:
                    node = foods_map[fid]
                    sel_chips.append({
                        "emoji": node.get('emoji','🍜') if isinstance(node, dict) else getattr(node, 'emoji', '🍜'),
                        "name": node.get('name','') if isinstance(node, dict) else getattr(node, 'name', '')
                    })
            
            if sel_chips:
                chip_cols = st.columns(len(sel_chips))
                for ci, sc in enumerate(sel_chips):
                    with chip_cols[ci]:
                        st.markdown(f"""<div style="display:flex;align-items:center;justify-content:center;gap:6px;background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.35);border-radius:999px;padding:7px 12px;font-size:0.8rem;font-weight:600;color:#F59E0B;text-align:center;white-space:nowrap;"><span>{sc['emoji']}</span><span>{sc['name']}</span></div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="btn-action">', unsafe_allow_html=True)
                if st.button("🔍 Cari Rekomendasi", use_container_width=True, key="btn_cari"):
                    with st.spinner("Menelusuri struktur graf..."):
                        try:
                            if "BFS" in algo:
                                recs = graph.bfs_recommend(st.session_state.selected_foods, max_depth=2, top_n=top_n)
                            else:
                                dfs_path = graph.dfs_explore(st.session_state.selected_foods[0], max_depth=3)
                                recs = []
                                for i, fid in enumerate(dfs_path):
                                    if fid not in st.session_state.selected_foods and fid in foods_map:
                                        node_raw = foods_map[fid]
                                        n_dict = node_raw if isinstance(node_raw, dict) else node_raw.__dict__
                                        recs.append({**n_dict, 'score': 1.0/(i+1), 'depth': i, 'reason': 'Jalur Eksplorasi DFS'})
                                recs = recs[:top_n]
                            st.session_state.recommendations = recs
                        except Exception as algo_err:
                            st.error(f"Algoritma penelusuran gagal: {algo_err}. Kemungkinan struktur graf internal Anda dimodifikasi.")
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="btn-reset">', unsafe_allow_html=True)
                if st.button("✕ Reset Pilihan", use_container_width=True, key="btn_reset"):
                    st.session_state.selected_foods = []
                    st.session_state.recommendations = []
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown("""<div class="section-header"><h3>Hasil Rekomendasi</h3><span class="section-tag">Output</span></div>""", unsafe_allow_html=True)

        if not st.session_state.recommendations:
            st.markdown("""<div class="empty-state"><div class="empty-state-icon">🍜</div><div class="empty-state-text">Belum ada rekomendasi</div><div class="empty-state-hint">Pilih makanan favoritmu di sebelah kiri,<br>lalu klik "Cari Rekomendasi"</div></div>""", unsafe_allow_html=True)
        else:
            algo_title = "BFS (Breadth-First Search)" if "BFS" in algo else "DFS (Depth-First Search)"
            st.markdown(f"""<div class="algo-banner"><strong>Algoritma: {algo_title}</strong><br>Ditemukan <strong>{len(st.session_state.recommendations)}</strong> hasil kecocokan graf.</div>""", unsafe_allow_html=True)

            valid_recs = [r for r in st.session_state.recommendations if (r.get('id') if isinstance(r, dict) else getattr(r, 'id', '')) in foods_map]
            
            if valid_recs:
                max_score = max((r.get('score', 1) if isinstance(r, dict) else getattr(r, 'score', 1)) for r in valid_recs) or 1
                
                for i, rec in enumerate(valid_recs):
                    is_d = isinstance(rec, dict)
                    r_id = rec.get('id') if is_d else getattr(rec, 'id')
                    r_name = rec.get('name') if is_d else getattr(rec, 'name')
                    r_emoji = rec.get('emoji', '🍜') if is_d else getattr(rec, 'emoji', '🍜')
                    r_cat = rec.get('category', '') if is_d else getattr(rec, 'category', '')
                    r_price = rec.get('price_range', 'murah') if is_d else getattr(rec, 'price_range', 'murah')
                    r_desc = rec.get('description', '') if is_d else getattr(rec, 'description', '')
                    r_tags = rec.get('tags', []) if is_d else getattr(rec, 'tags', [])
                    r_spicy = rec.get('spicy_level', 0) if is_d else getattr(rec, 'spicy_level', 0)
                    r_score = rec.get('score', 0) if is_d else getattr(rec, 'score', 0)
                    r_reason = rec.get('reason', 'Terhubung dalam kluster graf yang mirip') if is_d else getattr(rec, 'reason', 'Terhubung dalam kluster')

                    score_pct = int((r_score / max_score) * 100)
                    rank_display = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"

                    tags_html = '<div class="tag-container">'
                    for tag in r_tags:
                        tags_html += f'<span class="tag {str(tag).split()[0]}">{tag}</span>'
                    tags_html += '</div>'

                    spicy_html = '<div class="spicy-row"><span style="font-size:0.7rem;color:#475569;margin-right:4px;">PEDAS</span>'
                    for dot_i in range(5):
                        cls = "active" if dot_i < r_spicy else ""
                        spicy_html += f'<span class="spicy-dot {cls}"></span>'
                    spicy_html += '</div>'

                    price_color = {'murah': '#22C55E', 'sedang': '#F59E0B', 'mahal': '#EF4444'}.get(r_price.lower(), '#94A3B8')

                    st.markdown(f"""
                    <div class="rec-card">
                        <div style="display:flex;align-items:flex-start;justify-content:space-between;">
                            <div style="flex:1;">
                                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                                    <span style="font-size:1.5rem;">{r_emoji}</span>
                                    <div>
                                        <div class="rec-name">{r_name}</div>
                                        <div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.06em;">
                                            {r_cat.title()} · <span style="color:{price_color}">{r_price.title()}</span>
                                        </div>
                                    </div>
                                </div>
                                <div class="rec-desc">{r_desc}</div>
                                {tags_html}
                                {spicy_html}
                                <div class="score-bar-container">
                                    <div class="score-label">Skor Relasi Jalur</div>
                                    <div class="score-bar-track"><div class="score-bar-fill" style="width:{score_pct}%"></div></div>
                                </div>
                            </div>
                            <div class="rec-rank" style="margin-left:1rem;min-width:40px;text-align:right;">{rank_display}</div>
                        </div>
                        <div class="rec-reason">💡 {r_reason}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Bagian visualisasi Path antar node secara aman
            if "BFS" in algo and st.session_state.selected_foods and valid_recs:
                try:
                    source = st.session_state.selected_foods[0]
                    target = valid_recs[0].get('id') if isinstance(valid_recs[0], dict) else getattr(valid_recs[0], 'id')
                    if source in foods_map and target in foods_map:
                        path = graph.get_path_between(source, target)
                        if path:
                            st.markdown("""<div class="section-header" style="margin-top:1.5rem;"><h3>Jalur Koneksi Graf</h3><span class="section-tag">Shortest Path</span></div>""", unsafe_allow_html=True)
                            path_html = '<div class="path-trace">'
                            for pi, node_id in enumerate(path):
                                if node_id in foods_map:
                                    n_node = foods_map[node_id]
                                    n_emoji = n_node.get('emoji','🍜') if isinstance(n_node, dict) else getattr(n_node, 'emoji', '🍜')
                                    n_name = n_node.get('name','') if isinstance(n_node, dict) else getattr(n_node, 'name', '')
                                    path_html += f'<span class="path-node">{n_emoji} {n_name}</span>'
                                    if pi < len(path) - 1:
                                        path_html += '<span class="path-arrow">→</span>'
                            path_html += '</div>'
                            st.markdown(path_html, unsafe_allow_html=True)
                except Exception:
                    pass

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: VISUALISASI GRAF
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="section-header">
        <h3>Visualisasi Graf Makanan Interaktif</h3>
        <span class="section-tag">Network Canvas</span>
    </div>
    """, unsafe_allow_html=True)
    try:
        render_graph(graph, st.session_state.selected_foods)
    except Exception as viz_err:
        st.warning(f"Garis relasi graf sedang memproses penyesuaian node baru: {viz_err}")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: TENTANG ALGORITMA
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""<div class="section-header"><h3>Teori Dasar Struktur Data</h3></div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="rec-card">
        <div class="rec-name" style="color: var(--accent-gold);">Breadth-First Search (BFS)</div>
        <div class="rec-desc" style="font-size:0.85rem;">Menelusuri tetangga terdekat lapis demi lapis untuk akurasi rekomendasi kemiripan terbaik.</div>
    </div>
    <div class="rec-card">
        <div class="rec-name" style="color: var(--accent-orange);">Depth-First Search (DFS)</div>
        <div class="rec-desc" style="font-size:0.85rem;">Menjelajah jalur silsilah rasa terdalam ke kluster menu lain untuk kejutan rekomendasi unik.</div>
    </div>
    """, unsafe_allow_html=True)
