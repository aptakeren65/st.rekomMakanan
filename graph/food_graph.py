from collections import defaultdict, deque
import json
import os

    with st.expander("🛠️ MANAGE DATA GRAF (CRUD)"):
        crud_mode = st.radio("Aksi Graf", ["Lihat Data (Read)", "Tambah Node (Create)", "Update Node", "Hapus Node (Delete)"])
        
        # Menggunakan objek penampung sesuai file food_graph.py Anda
        foods_map = graph.foods if hasattr(graph, 'foods') else {}
        adj_data = graph.adjacency_list if hasattr(graph, 'adjacency_list') else {}

        # 1. READ
        if crud_mode == "Lihat Data (Read)":
            st.write("**Daftar Node Graf Saat Ini:**")
            if foods_map:
                for fid, f_data in foods_map.items():
                    st.text(f"[{fid}] {f_data.get('emoji','🍜')} {f_data.get('name','Tanpa Nama')}")
            else:
                st.warning("Data graf kosong.")
                
        # 2. CREATE
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
                            # Menyuntikkan field wajib default untuk visualisasi graf
                            new_node_data = {
                                "id": new_id, "name": new_name, "emoji": new_emoji,
                                "category": new_cat, "price_range": new_price,
                                "spicy_level": new_spicy, "description": new_desc, "tags": tag_list,
                                "image_color": "#F59E0B" # Warna default node baru agar tidak crash saat viz
                            }
                            try:
                                # Daftarkan ke class FoodGraph Anda
                                graph.add_node(new_node_data)
                                
                                # Inisialisasi list tetangga kosong di defaultdict asli Anda
                                if new_id not in adj_data:
                                    adj_data[new_id] = []
                                        
                                st.success(f"Berhasil menambahkan node: {new_name}!")
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Gagal menyimpan data ke graf: {ex}")
                    else:
                        st.error("ID dan Nama Makanan wajib diisi!")

        # 3. UPDATE
        elif crud_mode == "Update Node":
            if foods_map:
                target_update_id = st.selectbox("Pilih ID Node", options=list(foods_map.keys()))
                if target_update_id:
                    current_node = foods_map[target_update_id]

                    with st.form("update_node_form"):
                        up_name = st.text_input("Nama Makanan", value=current_node.get('name', ''))
                        up_emoji = st.text_input("Emoji", value=current_node.get('emoji', ''))
                        up_cat = st.text_input("Kategori", value=current_node.get('category', ''))
                        up_price = st.selectbox("Harga", ["murah", "sedang", "mahal"], index=["murah", "sedang", "mahal"].index(current_node.get('price_range', 'murah')))
                        up_spicy = st.slider("Level Pedas", 0, 5, int(current_node.get('spicy_level', 0)))
                        up_desc = st.text_area("Deskripsi", value=current_node.get('description', ''))
                        up_tags = st.text_input("Tags (Koma)", value=", ".join(current_node.get('tags', [])))
                        
                        if st.form_submit_button("Simpan Perubahan"):
                            current_node.update({
                                "name": up_name, "emoji": up_emoji, "category": up_cat.lower(),
                                "price_range": up_price, "spicy_level": up_spicy, "description": up_desc,
                                "tags": [t.strip() for t in up_tags.split(",") if t.strip()]
                            })
                            st.success("Node berhasil diperbarui!")
                            st.rerun()
            else:
                st.warning("Tidak ada node yang tersedia.")

        # 4. DELETE
        elif crud_mode == "Hapus Node (Delete)":
            if foods_map:
                target_del_id = st.selectbox("Pilih ID Node untuk Dihapus", options=list(foods_map.keys()))
                if st.button("🔴 Eksekusi Hapus", use_container_width=True):
                    try:
                        # 1. Hapus dari daftar makanan utama
                        if target_del_id in foods_map:
                            del foods_map[target_del_id]
                        
                        # 2. Hapus total node dan relasi keluar-masuk dari adjacency_list asli Anda
                        if target_del_id in adj_data:
                            del adj_data[target_del_id]
                        
                        for k, v in adj_data.items():
                            adj_data[k] = [edge for edge in v if edge[0] != target_del_id]
                                    
                        if target_del_id in st.session_state.selected_foods:
                            st.session_state.selected_foods.remove(target_del_id)
                            
                        st.success("Node dan relasinya berhasil dihapus bersih!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Gagal menghapus node: {ex}")
            else:
                st.warning("Tidak ada data untuk dihapus.")r v in self.adjacency_list.values())
        return total // 2  # undirected
