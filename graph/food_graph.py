from collections import defaultdict, deque
import json
import os


class FoodGraph:
    """
    Graf makanan menggunakan Adjacency List (Weighted & Undirected)
    Setiap node = makanan, setiap edge = relasi antar makanan
    """

    def __init__(self):
        self.adjacency_list = defaultdict(list)  # {food_id: [(neighbor_id, weight, reason)]}
        self.foods = {}  # {food_id: food_data}
        self._load_data()

    def _load_data(self):
        """Load data makanan dari JSON dan bangun graph"""
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'foods.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Masukkan semua node
        for food in data['foods']:
            self.add_node(food)

        # Masukkan semua edge (undirected)
        for rel in data['relations']:
            self.add_edge(rel['from'], rel['to'], rel['weight'], rel['reason'])

    def add_node(self, food_data: dict):
        """Tambah node (makanan) ke graph"""
        self.foods[food_data['id']] = food_data

    def add_edge(self, food_a: str, food_b: str, weight: float = 1.0, reason: str = ""):
        """Tambah edge antara dua makanan (undirected)"""
        self.adjacency_list[food_a].append((food_b, weight, reason))
        self.adjacency_list[food_b].append((food_a, weight, reason))

    def get_neighbors(self, food_id: str) -> list:
        """Ambil semua tetangga dari sebuah node"""
        return self.adjacency_list.get(food_id, [])

    def bfs_recommend(self, start_ids: list, max_depth: int = 2, top_n: int = 8) -> list:
        """
        BFS dari beberapa node awal sekaligus
        Mengembalikan rekomendasi berdasarkan jarak dan bobot edge
        
        Returns: [(food_id, score, depth, reason)]
        """
        visited = set(start_ids)
        scores = {}  # {food_id: (score, depth, reason)}
        queue = deque()

        # Masukkan semua start node ke queue
        for start_id in start_ids:
            if start_id in self.foods:
                visited.add(start_id)
                for neighbor, weight, reason in self.get_neighbors(start_id):
                    if neighbor not in visited:
                        queue.append((neighbor, 1, weight, reason))

        while queue:
            food_id, depth, score, reason = queue.popleft()

            if depth > max_depth:
                continue

            if food_id not in visited:
                visited.add(food_id)
                # Bobot skor: semakin dekat, semakin tinggi
                depth_penalty = 1.0 / depth
                final_score = score * depth_penalty

                if food_id not in scores or final_score > scores[food_id][0]:
                    scores[food_id] = (final_score, depth, reason)

                # Lanjut BFS ke tetangga berikutnya
                for neighbor, weight, reason in self.get_neighbors(food_id):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1, weight, reason))

        # Sort berdasarkan score tertinggi
        results = [
            {
                **self.foods[fid],
                'score': s[0],
                'depth': s[1],
                'reason': s[2]
            }
            for fid, s in scores.items()
            if fid in self.foods
        ]
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_n]

    def dfs_explore(self, start_id: str, visited=None, depth=0, max_depth=3) -> list:
        """
        DFS dari node awal - menjelajahi jalur terpanjang satu keluarga rasa
        Returns: list of food_ids dalam urutan traversal DFS
        """
        if visited is None:
            visited = set()

        if start_id in visited or depth > max_depth:
            return []

        visited.add(start_id)
        path = [start_id]

        # Urutkan tetangga berdasarkan bobot (greedy DFS)
        neighbors = sorted(
            self.get_neighbors(start_id),
            key=lambda x: x[1],
            reverse=True
        )

        for neighbor_id, weight, reason in neighbors:
            if neighbor_id not in visited:
                sub_path = self.dfs_explore(neighbor_id, visited, depth + 1, max_depth)
                path.extend(sub_path)

        return path

    def get_path_between(self, source: str, target: str) -> list:
        """BFS untuk menemukan jalur terpendek antara dua makanan"""
        if source == target:
            return [source]

        visited = {source}
        queue = deque([(source, [source])])

        while queue:
            current, path = queue.popleft()
            for neighbor, _, _ in self.get_neighbors(current):
                if neighbor == target:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []

    def filter_foods(self, category=None, tags=None, max_spicy=5, price_range=None) -> list:
        """Filter makanan berdasarkan kriteria"""
        results = []
        for food_id, food in self.foods.items():
            if category and food['category'] != category:
                continue
            if tags and not any(t in food['tags'] for t in tags):
                continue
            if food['spicy_level'] > max_spicy:
                continue
            if price_range and food['price_range'] != price_range:
                continue
            results.append(food)
        return results

    def get_graph_data_for_viz(self, highlight_ids=None) -> dict:
        """Export data graph untuk visualisasi pyvis/networkx"""
        nodes = []
        edges = []
        seen_edges = set()

        for food_id, food in self.foods.items():
            is_highlighted = highlight_ids and food_id in highlight_ids
            nodes.append({
                'id': food_id,
                'label': food['name'],
                'emoji': food['emoji'],
                'color': food['image_color'],
                'highlighted': is_highlighted,
                'category': food['category'],
                'spicy': food['spicy_level']
            })

        for food_id in self.adjacency_list:
            for neighbor_id, weight, reason in self.adjacency_list[food_id]:
                edge_key = tuple(sorted([food_id, neighbor_id]))
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    edges.append({
                        'from': food_id,
                        'to': neighbor_id,
                        'weight': weight,
                        'reason': reason,
                        'highlighted': highlight_ids and (food_id in highlight_ids or neighbor_id in highlight_ids)
                    })

        return {'nodes': nodes, 'edges': edges}

    def get_all_categories(self) -> list:
        cats = list(set(f['category'] for f in self.foods.values()))
        return sorted(cats)

    def get_all_tags(self) -> list:
        tags = set()
        for f in self.foods.values():
            tags.update(f['tags'])
        return sorted(list(tags))

    def total_nodes(self) -> int:
        return len(self.foods)

    def total_edges(self) -> int:
        total = sum(len(v) for v in self.adjacency_list.values())
        return total // 2  # undirected
