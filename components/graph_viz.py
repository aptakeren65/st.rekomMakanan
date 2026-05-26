import streamlit.components.v1 as components
from pyvis.network import Network
import tempfile
import os


def render_graph(graph_data: dict, height: int = 500):
    """Render interactive graph menggunakan PyVis"""

    net = Network(
        height=f"{height}px",
        width="100%",
        bgcolor="#0F172A",
        font_color="#F8FAFC",
        directed=False
    )

    net.set_options("""
    {
      "nodes": {
        "borderWidth": 2,
        "borderWidthSelected": 4,
        "shadow": {
          "enabled": true,
          "color": "rgba(0,0,0,0.5)",
          "size": 15,
          "x": 3,
          "y": 3
        },
        "font": {
          "size": 13,
          "face": "Georgia",
          "bold": {
            "face": "Georgia"
          }
        }
      },
      "edges": {
        "color": {
          "inherit": false
        },
        "smooth": {
          "enabled": true,
          "type": "continuous",
          "roundness": 0.3
        },
        "shadow": false
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "hideEdgesOnDrag": false,
        "navigationButtons": false
      },
      "physics": {
        "enabled": true,
        "stabilization": {
          "enabled": true,
          "iterations": 200
        },
        "barnesHut": {
          "gravitationalConstant": -8000,
          "centralGravity": 0.3,
          "springLength": 120,
          "springConstant": 0.04,
          "damping": 0.09
        }
      }
    }
    """)

    # Tambah node
    for node in graph_data['nodes']:
        if node['highlighted']:
            size = 45
            border_color = "#FBBF24"
            bg_color = node['color']
            font_size = 15
        else:
            size = 30
            border_color = "#334155"
            bg_color = node['color'] + "99"  # semi-transparent
            font_size = 12

        label = f"{node['emoji']} {node['label']}"
        net.add_node(
            node['id'],
            label=label,
            title=f"<b>{node['label']}</b><br>Kategori: {node['category']}<br>Level Pedas: {'🌶️' * node['spicy']}",
            size=size,
            color={
                'background': bg_color,
                'border': border_color,
                'highlight': {'background': node['color'], 'border': '#FBBF24'}
            },
            font={'size': font_size, 'color': '#F8FAFC'}
        )

    # Tambah edge
    for edge in graph_data['edges']:
        width = edge['weight'] * 4
        if edge.get('highlighted'):
            color = "#FBBF24"
            width = edge['weight'] * 6
        else:
            color = "#1E3A5F"

        net.add_edge(
            edge['from'],
            edge['to'],
            width=width,
            color=color,
            title=edge['reason']
        )

    # Simpan ke temp file dan render (Windows-safe)
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8')
    tmp_path = tmp_file.name
    tmp_file.close()  # Tutup dulu agar Windows tidak mengunci file

    net.save_graph(tmp_path)

    with open(tmp_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    try:
        os.unlink(tmp_path)
    except Exception:
        pass  # Abaikan jika gagal hapus, tidak mempengaruhi tampilan

    components.html(html_content, height=height + 20, scrolling=False)
