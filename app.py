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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

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

/* ── Hide Streamlit branding ── */
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

/* ── Food Cards (pill grid) ── */
.food-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 0.5rem;
}

.food-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--bg-card);
    border: 1.5px solid var(--border);
    border-radius: 999px;
    padding: 8px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-secondary);
    user-select: none;
}
.food-pill:hover {
    border-color: var(--accent-gold);
    background: var(--bg-card-hover);
    color: var(--text-primary);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(245,158,11,0.15);
}
.food-pill.selected {
    border-color: var(--accent-gold);
    background: rgba(245,158,11,0.12);
    color: var(--accent-gold);
    font-weight: 600;
    box-shadow: 0 0 0 1px rgba(245,158,11,0.25), 0 4px 12px rgba(245,158,11,0.2);
}

/* ── Recommendation Cards ── */
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
.score-bar-container {
    margin: 0.5rem 0;
}
.score-bar-track {
    background: var(--border);
    height: 4px;
    border-radius: 999px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #F59E0B, #EA580C);
    border-radius: 999px;
    transition: width 1s ease;
}
.score-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-bottom: 4px;
}

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
.spicy-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--border);
}
.spicy-dot.active { background: #EF4444; }

/* ── Stats Cards ── */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #F59E0B, #EA580C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 0.35rem;
}

/* ── Divider ── */
.fancy-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-accent), transparent);
    margin: 1.5rem 0;
}

/* ── Empty State ── */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    border: 1px dashed var(--border);
    border-radius: var(--radius-lg);
}
.empty-state-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
}
.empty-state-hint { font-size: 0.85rem; color: var(--text-muted); }

/* ── Sidebar overrides ── */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div > div {
    background: var(--accent-gold) !important;
}
[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
    background-color: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    padding: 0.75rem 1.5rem !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-gold) !important;
    border-bottom-color: var(--accent-gold) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding-top: 1.5rem !important;
}

/* ── Action Buttons (Cari, Reset) ── */
div[data-testid="stButton"].action-btn > button,
.action-btn button {
    background: linear-gradient(135deg, #F59E0B, #EA580C) !important;
    color: #0F0F0F !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.2s ease !important;
}

/* ── Food Card Buttons ── */
/* Semua button default: style kartu makanan */
.stButton > button {
    background: #111827 !important;
    color: #94A3B8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    border: 1.5px solid #1E293B !important;
    border-radius: 12px !important;
    padding: 0.9rem 0.5rem !important;
    transition: all 0.2s ease !important;
    white-space: pre-wrap !important;
    line-height: 1.5 !important;
    height: auto !important;
    min-height: 90px !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    border-color: #F59E0B !important;
    background: #1A2538 !important;
    color: #F8FAFC !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(245,158,11,0.2) !important;
}
/* Selected state via data attribute workaround: pakai class selector */
button[data-selected="true"] {
    background: rgba(245,158,11,0.1) !important;
    border-color: #F59E0B !important;
    color: #F59E0B !important;
    box-shadow: 0 0 0 1px rgba(245,158,11,0.25) !important;
}

/* ── Override untuk tombol Cari & Reset (wrapper khusus) ── */
.btn-action .stButton > button {
    background: linear-gradient(135deg, #F59E0B, #EA580C) !important;
    color: #0F0F0F !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.65rem 1.5rem !important;
    min-height: unset !important;
    height: auto !important;
    transform: none !important;
}
.btn-action .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(245,158,11,0.4) !important;
    filter: brightness(1.1) !important;
    border: none !important;
}
.btn-reset .stButton > button {
    background: #1E293B !important;
    color: #94A3B8 !important;
    border: 1px solid #334155 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.65rem 1.5rem !important;
    min-height: unset !important;
    height: auto !important;
}
.btn-reset .stButton > button:hover {
    background: #273548 !important;
    color: #F8FAFC !important;
    border-color: #475569 !important;
    transform: none !important;
    box-shadow: none !important;
    filter: none !important;
}

/* ── Path trace ── */
.path-trace {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 6px;
    padding: 1rem 1.25rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    margin-top: 1rem;
}
.path-node {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--accent-gold);
    background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.2);
    padding: 4px 12px;
    border-radius: 999px;
}
.path-arrow { color: var(--text-muted); font-size: 0.9rem; }

/* ── Info Banner ── */
.algo-banner {
    background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(234,88,12,0.08));
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: var(--radius-md);
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.6;
}
.algo-banner strong { color: var(--accent-gold); }
</style>
""", unsafe_allow_html=True)


# ─── INIT GRAPH ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_graph():
    return FoodGraph()

graph = load_graph()
all_foods = list(graph.foods.values())


# ─── SESSION STATE ────────────────────────────────────────────────────────────
if 'selected_foods' not in st.session_state:
    st.session_state.selected_foods = []
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0


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
        <div style="font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;
                    color:#475569;margin-top:4px;">
            Struktur Data — Graph
        </div>
    </div>
    <hr style="border:none;border-top:1px solid #1E293B;margin:0 0 1.5rem;">
    """, unsafe_allow_html=True)

    # ── Filter Kategori
    st.markdown("<label>Kategori</label>", unsafe_allow_html=True)
    categories = ["Semua"] + [c.title() for c in graph.get_all_categories()]
    selected_category = st.selectbox("Kategori", categories, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Level Kepedasan
    st.markdown("<label>Maks. Level Pedas</label>", unsafe_allow_html=True)
    spicy_icons = ["0 — Tidak Pedas", "1 — Sedikit Pedas", "2 — Sedang", "3 — Pedas", "4 — Sangat Pedas", "5 — Ekstrem"]
    max_spicy = st.slider("Pedas", 0, 5, 5, label_visibility="collapsed",
                          format="%d 🌶️")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Harga
    st.markdown("<label>Kisaran Harga</label>", unsafe_allow_html=True)
    price_opts = ["Semua", "Murah", "Sedang", "Mahal"]
    selected_price = st.selectbox("Harga", price_opts, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Algoritma
    st.markdown("<label>Algoritma</label>", unsafe_allow_html=True)
    algo = st.radio(
        "Algoritma",
        ["BFS (Rekomendasi Cepat)", "DFS (Eksplorasi Mendalam)"],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Max Rekomendasi
    st.markdown("<label>Jumlah Rekomendasi</label>", unsafe_allow_html=True)
    top_n = st.slider("Top N", 3, 12, 6, label_visibility="collapsed")

    # ── Stats di sidebar bawah
    st.markdown("""<hr style="border:none;border-top:1px solid #1E293B;margin:1.5rem 0;">""",
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{graph.total_nodes()}</div>
            <div class="stat-label">Makanan</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{graph.total_edges()}</div>
            <div class="stat-label">Relasi</div>
        </div>
        """, unsafe_allow_html=True)


# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────

# Hero Header
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

# ── Tabs
tab1, tab2, tab3 = st.tabs(["🔍  Rekomendasi", "🕸️  Graf Interaktif", "📚  Tentang Algoritma"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: REKOMENDASI
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:

    col_left, col_right = st.columns([1.1, 0.9], gap="large")

    with col_left:

        # ── Filter makanan untuk ditampilkan
        cat_filter = None if selected_category == "Semua" else selected_category.lower()
        price_filter = None if selected_price == "Semua" else selected_price.lower()
        filtered_foods = graph.filter_foods(
            category=cat_filter,
            max_spicy=max_spicy,
            price_range=price_filter
        )

        st.markdown("""
        <div class="section-header">
            <h3>Pilih Makanan Favorit</h3>
            <span class="section-tag">Pilih 1-5</span>
        </div>
        """, unsafe_allow_html=True)

        if not filtered_foods:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <div class="empty-state-text">Tidak ada makanan ditemukan</div>
                <div class="empty-state-hint">Coba ubah filter di sidebar</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Render pill buttons per food
            n_cols = 3
            pills_per_row = [filtered_foods[i:i+n_cols] for i in range(0, len(filtered_foods), n_cols)]

            for row in pills_per_row:
                cols = st.columns(len(row))
                for col, food in zip(cols, row):
                    with col:
                        is_sel = food['id'] in st.session_state.selected_foods

                        # Buat spicy indicator pakai teks unicode (aman di button label)
                        spicy_filled = food['spicy_level']
                        spicy_str = "🔴" * spicy_filled + "⚫" * (5 - spicy_filled) if spicy_filled > 0 else "⚫⚫⚫⚫⚫"

                        check = "✓  " if is_sel else ""
                        label = f"{food['emoji']}\n{check}{food['name']}\n{spicy_str}"

                        # Inject CSS class per-button berdasarkan selected state
                        sel_style = ""
                        if is_sel:
                            sel_style = f"""
                            <style>
                            div[data-testid="stButton"]:has(button[kind="secondary"][title="{food['description']}"]) > button {{
                                background: rgba(245,158,11,0.12) !important;
                                border-color: #F59E0B !important;
                                color: #F59E0B !important;
                                box-shadow: 0 0 0 1px rgba(245,158,11,0.25), 0 4px 12px rgba(245,158,11,0.15) !important;
                            }}
                            </style>
                            """
                            st.markdown(sel_style, unsafe_allow_html=True)

                        if st.button(label, key=f"pill_{food['id']}",
                                     help=food['description'],
                                     use_container_width=True):
                            if food['id'] in st.session_state.selected_foods:
                                st.session_state.selected_foods.remove(food['id'])
                            elif len(st.session_state.selected_foods) < 5:
                                st.session_state.selected_foods.append(food['id'])
                            st.rerun()

        # ── Selected summary
        if st.session_state.selected_foods:
            st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
            st.markdown("""
            <div class="section-header">
                <h3>Makanan Dipilih</h3>
            </div>
            """, unsafe_allow_html=True)

            # Tampilkan chips makanan dipilih menggunakan kolom Streamlit
            sel_foods_data = [graph.foods[fid] for fid in st.session_state.selected_foods if fid in graph.foods]
            if sel_foods_data:
                chip_cols = st.columns(len(sel_foods_data))
                for ci, sf in enumerate(sel_foods_data):
                    with chip_cols[ci]:
                        st.markdown(f"""
                        <div style="
                            display:flex;align-items:center;justify-content:center;gap:6px;
                            background:rgba(245,158,11,0.1);
                            border:1px solid rgba(245,158,11,0.35);
                            border-radius:999px;
                            padding:7px 12px;
                            font-size:0.8rem;font-weight:600;
                            color:#F59E0B;text-align:center;
                            white-space:nowrap;
                        ">
                            <span>{sf['emoji']}</span><span>{sf['name']}</span>
                        </div>
                        """, unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="btn-action">', unsafe_allow_html=True)
                if st.button("🔍 Cari Rekomendasi", use_container_width=True, key="btn_cari"):
                    with st.spinner("Menjalankan algoritma..."):
                        if "BFS" in algo:
                            recs = graph.bfs_recommend(
                                st.session_state.selected_foods,
                                max_depth=2,
                                top_n=top_n
                            )
                        else:
                            dfs_path = graph.dfs_explore(
                                st.session_state.selected_foods[0],
                                max_depth=3
                            )
                            recs = [
                                {**graph.foods[fid], 'score': 1.0/(i+1), 'depth': i, 'reason': 'jalur DFS'}
                                for i, fid in enumerate(dfs_path)
                                if fid not in st.session_state.selected_foods
                                and fid in graph.foods
                            ][:top_n]
                    st.session_state.recommendations = recs
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="btn-reset">', unsafe_allow_html=True)
                if st.button("✕ Reset Pilihan", use_container_width=True, key="btn_reset"):
                    st.session_state.selected_foods = []
                    st.session_state.recommendations = []
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # ── RIGHT COLUMN: Recommendations
    with col_right:

        st.markdown("""
        <div class="section-header">
            <h3>Hasil Rekomendasi</h3>
            <span class="section-tag">Hasil</span>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.recommendations:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🍜</div>
                <div class="empty-state-text">Belum ada rekomendasi</div>
                <div class="empty-state-hint">Pilih makanan favoritmu di sebelah kiri,<br>lalu klik "Cari Rekomendasi"</div>
            </div>
            """, unsafe_allow_html=True)

        else:
            # Algorithm info banner
            algo_name = "BFS (Breadth-First Search)" if "BFS" in algo else "DFS (Depth-First Search)"
            st.markdown(f"""
            <div class="algo-banner">
                <strong>Algoritma: {algo_name}</strong><br>
                Ditemukan <strong>{len(st.session_state.recommendations)}</strong> rekomendasi
                berdasarkan <strong>{len(st.session_state.selected_foods)}</strong> makanan pilihan.
            </div>
            """, unsafe_allow_html=True)

            max_score = max(r['score'] for r in st.session_state.recommendations) or 1

            for i, rec in enumerate(st.session_state.recommendations):
                score_pct = int((rec['score'] / max_score) * 100)
                rank_class = "top" if i < 3 else ""
                rank_display = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"

                # Tags
                tags_html = '<div class="tag-container">'
                for tag in rec.get('tags', []):
                    tags_html += f'<span class="tag {tag.split()[0]}">{tag}</span>'
                tags_html += '</div>'

                # Spicy
                spicy_html = '<div class="spicy-row">'
                spicy_html += '<span style="font-size:0.7rem;color:#475569;margin-right:4px;">PEDAS</span>'
                for dot_i in range(5):
                    cls = "active" if dot_i < rec.get('spicy_level', 0) else ""
                    spicy_html += f'<span class="spicy-dot {cls}"></span>'
                spicy_html += '</div>'

                price_colors = {'murah': '#22C55E', 'sedang': '#F59E0B', 'mahal': '#EF4444'}
                price_color = price_colors.get(rec.get('price_range', ''), '#94A3B8')

                st.markdown(f"""
                <div class="rec-card">
                    <div style="display:flex;align-items:flex-start;justify-content:space-between;">
                        <div style="flex:1;">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                                <span style="font-size:1.5rem;">{rec['emoji']}</span>
                                <div>
                                    <div class="rec-name">{rec['name']}</div>
                                    <div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.06em;">
                                        {rec.get('category','').title()} ·
                                        <span style="color:{price_color}">
                                            {rec.get('price_range','').title()}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="rec-desc">{rec['description']}</div>
                            {tags_html}
                            {spicy_html}
                            <div class="score-bar-container">
                                <div class="score-label">Skor Kemiripan</div>
                                <div class="score-bar-track">
                                    <div class="score-bar-fill" style="width:{score_pct}%"></div>
                                </div>
                            </div>
                        </div>
                        <div class="rec-rank {rank_class}" style="margin-left:1rem;min-width:40px;text-align:right;">
                            {rank_display}
                        </div>
                    </div>
                    <div class="rec-reason">💡 {rec.get('reason','Terhubung dalam graph')}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Path tracer (BFS only)
            if "BFS" in algo and st.session_state.selected_foods and st.session_state.recommendations:
                st.markdown("""
                <div class="section-header" style="margin-top:1.5rem;">
                    <h3>Jalur Koneksi</h3>
                    <span class="section-tag">BFS Path</span>
                </div>
                """, unsafe_allow_html=True)

                source = st.session_state.selected_foods[0]
                target = st.session_state.recommendations[0]['id']
                path = graph.get_path_between(source, target)

                if path:
                    path_html = '<div class="path-trace">'
                    for pi, node_id in enumerate(path):
                        food_n = graph.foods.get(node_id, {})
                        path_html += f'<span class="path-node">{food_n.get("emoji","")} {food_n.get("name","")}</span>'
                        if pi < len(path) - 1:
                            path_html += '<span class="path-arrow">→</span>'
                    path_html += '</div>'
                    st.markdown(path_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: GRAPH VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:

    st.markdown("""
    <div class="section-header">
        <h3>Visualisasi Graf Makanan</h3>
        <span class="section-tag">Interaktif</span>
    </div>
    <p style="color:#64748B;font-size:0.85rem;margin-bottom:1.5rem;">
        Graf lengkap semua makanan dan relasinya. Node berwarna emas = makanan yang dipilih.
        Hover untuk melihat info. Drag untuk eksplorasi.
    </p>
    """, unsafe_allow_html=True)

    # Legend
    legend_col1, legend_col2, legend_col3 = st.columns(3)
    with legend_col1:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size:0.7rem;letter-spacing:0.08em;text-transform:uppercase;color:#475569;margin-bottom:8px;">Node</div>
            <div style="font-size:0.85rem;color:#94A3B8;">Setiap lingkaran = 1 makanan</div>
        </div>
        """, unsafe_allow_html=True)
    with legend_col2:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size:0.7rem;letter-spacing:0.08em;text-transform:uppercase;color:#475569;margin-bottom:8px;">Edge</div>
            <div style="font-size:0.85rem;color:#94A3B8;">Garis = relasi antar makanan</div>
        </div>
        """, unsafe_allow_html=True)
    with legend_col3:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size:0.7rem;letter-spacing:0.08em;text-transform:uppercase;color:#475569;margin-bottom:8px;">Ketebalan</div>
            <div style="font-size:0.85rem;color:#94A3B8;">Lebih tebal = lebih mirip</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    highlight_set = set(st.session_state.selected_foods)
    if st.session_state.recommendations:
        highlight_set.update(r['id'] for r in st.session_state.recommendations[:3])

    graph_data = graph.get_graph_data_for_viz(
        highlight_ids=highlight_set if highlight_set else None
    )

    render_graph(graph_data, height=560)

    st.markdown("""
    <div style="text-align:center;color:#475569;font-size:0.75rem;margin-top:1rem;
                letter-spacing:0.05em;">
        SCROLL UNTUK ZOOM · DRAG NODE UNTUK EKSPLORASI · HOVER UNTUK DETAIL
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: ABOUT ALGORITHM
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:

    col_bfs, col_dfs = st.columns(2, gap="large")

    with col_bfs:
        st.markdown("""
        <div style="background:#111827;border:1px solid #1E293B;border-radius:14px;padding:1.5rem;height:100%;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;">
                <div style="background:rgba(245,158,11,0.15);border:1px solid rgba(245,158,11,0.3);
                            border-radius:8px;width:40px;height:40px;display:flex;align-items:center;
                            justify-content:center;font-size:1.2rem;">🌊</div>
                <div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
                                color:#F8FAFC;">BFS</div>
                    <div style="font-size:0.7rem;color:#475569;letter-spacing:0.08em;text-transform:uppercase;">
                        Breadth-First Search
                    </div>
                </div>
            </div>
            <p style="color:#94A3B8;font-size:0.85rem;line-height:1.7;">
                BFS menjelajahi graf lapis per lapis — semua tetangga langsung (level 1) 
                dikunjungi terlebih dahulu, baru kemudian tetangga dari tetangga (level 2), 
                dan seterusnya.
            </p>
            <div style="background:#0F172A;border-radius:8px;padding:1rem;margin:1rem 0;
                        font-family:monospace;font-size:0.78rem;color:#7DD3FC;line-height:1.8;">
                Queue: [Nasi Goreng]<br>
                Level 1: Nasi Uduk, Mie Goreng<br>
                Level 2: Nasi Kuning, Bakso<br>
                → Rekomendasi terurut!
            </div>
            <div style="border-top:1px solid #1E293B;padding-top:1rem;">
                <div style="font-size:0.75rem;color:#475569;text-transform:uppercase;
                            letter-spacing:0.08em;margin-bottom:0.5rem;">Kompleksitas</div>
                <div style="font-size:0.85rem;color:#94A3B8;">
                    ⏱ Waktu: <span style="color:#FCD34D;">O(V + E)</span><br>
                    💾 Ruang: <span style="color:#FCD34D;">O(V)</span>
                </div>
            </div>
            <div style="margin-top:1rem;">
                <div style="font-size:0.75rem;color:#475569;text-transform:uppercase;
                            letter-spacing:0.08em;margin-bottom:0.5rem;">Cocok Untuk</div>
                <div style="font-size:0.85rem;color:#94A3B8;line-height:1.6;">
                    ✅ Rekomendasi paling mirip<br>
                    ✅ Jalur terpendek antar makanan<br>
                    ✅ Hasil cepat & terurut
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_dfs:
        st.markdown("""
        <div style="background:#111827;border:1px solid #1E293B;border-radius:14px;padding:1.5rem;height:100%;">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:1rem;">
                <div style="background:rgba(234,88,12,0.15);border:1px solid rgba(234,88,12,0.3);
                            border-radius:8px;width:40px;height:40px;display:flex;align-items:center;
                            justify-content:center;font-size:1.2rem;">🌿</div>
                <div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
                                color:#F8FAFC;">DFS</div>
                    <div style="font-size:0.7rem;color:#475569;letter-spacing:0.08em;text-transform:uppercase;">
                        Depth-First Search
                    </div>
                </div>
            </div>
            <p style="color:#94A3B8;font-size:0.85rem;line-height:1.7;">
                DFS menyelam sejauh mungkin ke satu cabang sebelum mundur dan mencoba 
                cabang lain. Menggunakan rekursi, ia menjelajahi satu "keluarga rasa" 
                secara mendalam sebelum pindah ke kelompok makanan lain.
            </p>
            <div style="background:#0F172A;border-radius:8px;padding:1rem;margin:1rem 0;
                        font-family:monospace;font-size:0.78rem;color:#86EFAC;line-height:1.8;">
                Stack: [Rendang]<br>
                → Kalio → Opor Ayam<br>
                → kembali... Soto Betawi<br>
                → Eksplorasi mendalam!
            </div>
            <div style="border-top:1px solid #1E293B;padding-top:1rem;">
                <div style="font-size:0.75rem;color:#475569;text-transform:uppercase;
                            letter-spacing:0.08em;margin-bottom:0.5rem;">Kompleksitas</div>
                <div style="font-size:0.85rem;color:#94A3B8;">
                    ⏱ Waktu: <span style="color:#FCD34D;">O(V + E)</span><br>
                    💾 Ruang: <span style="color:#FCD34D;">O(H)</span> — H = kedalaman
                </div>
            </div>
            <div style="margin-top:1rem;">
                <div style="font-size:0.75rem;color:#475569;text-transform:uppercase;
                            letter-spacing:0.08em;margin-bottom:0.5rem;">Cocok Untuk</div>
                <div style="font-size:0.85rem;color:#94A3B8;line-height:1.6;">
                    ✅ Eksplorasi satu keluarga masakan<br>
                    ✅ Menemukan makanan tersembunyi<br>
                    ✅ Pakai memori lebih hemat
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Graph theory explanation
    st.markdown("""
    <div style="background:#111827;border:1px solid #1E293B;border-radius:14px;padding:1.75rem;">
        <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;
                    color:#F8FAFC;margin-bottom:1rem;">🕸️ Struktur Data Graf yang Digunakan</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;">
            <div>
                <div style="font-size:0.7rem;color:#F59E0B;text-transform:uppercase;
                            letter-spacing:0.08em;font-weight:600;margin-bottom:0.5rem;">Representasi</div>
                <div style="font-size:0.85rem;color:#94A3B8;line-height:1.6;">
                    <strong style="color:#F8FAFC">Adjacency List</strong><br>
                    Dict Python dengan key = food_id dan value = list tetangga beserta bobot dan alasan relasi.
                </div>
            </div>
            <div>
                <div style="font-size:0.7rem;color:#F59E0B;text-transform:uppercase;
                            letter-spacing:0.08em;font-weight:600;margin-bottom:0.5rem;">Jenis Graf</div>
                <div style="font-size:0.85rem;color:#94A3B8;line-height:1.6;">
                    <strong style="color:#F8FAFC">Undirected + Weighted</strong><br>
                    Relasi bersifat dua arah. Bobot 0.0–1.0 mewakili tingkat kemiripan antar makanan.
                </div>
            </div>
            <div>
                <div style="font-size:0.7rem;color:#F59E0B;text-transform:uppercase;
                            letter-spacing:0.08em;font-weight:600;margin-bottom:0.5rem;">Ukuran Graf</div>
                <div style="font-size:0.85rem;color:#94A3B8;line-height:1.6;">
                    <strong style="color:#F8FAFC">{nodes} Node, {edges} Edge</strong><br>
                    Setiap node = makanan. Setiap edge = satu relasi. Total {total} koneksi tersimpan dalam list.
                </div>
            </div>
        </div>
    </div>
    """.format(
        nodes=graph.total_nodes(),
        edges=graph.total_edges(),
        total=graph.total_edges() * 2  # undirected stored twice
    ), unsafe_allow_html=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<hr class="fancy-divider" style="margin-top:3rem;">
<div style="text-align:center;padding:1rem 0 2rem;">
    <div style="font-family:'Playfair Display',serif;font-size:0.9rem;color:#334155;">
        🍽️ FoodGraph &nbsp;·&nbsp; Tugas Mata Kuliah Struktur Data
    </div>
    <div style="font-size:0.75rem;color:#1E293B;margin-top:4px;letter-spacing:0.08em;text-transform:uppercase;">
        Graph · BFS · DFS · Adjacency List · Python + Streamlit
    </div>
</div>
""", unsafe_allow_html=True)
