import heapq

def ucs(graph, start, goal):
    # Inisialisasi antrian prioritas dengan simpul awal dan biaya awal 0
    priority_queue = [(0, start)]
    
    # Inisialisasi set untuk melacak simpul yang sudah dikunjungi
    visited = set()
    
    # Inisialisasi kamus untuk melacak biaya terendah ke setiap simpul
    path_cost = {node: float('inf') for node in graph}
    path_cost[start] = 0
    
    # Inisialisasi kamus untuk melacak jalur dari simpul awal ke simpul lain
    path = {start: None}
    
    while priority_queue:
        # Ambil simpul dengan biaya terendah dari antrian prioritas
        current_cost, current_node = heapq.heappop(priority_queue)
        
        # Jika sudah mencapai tujuan, kembalikan jalur dan biaya terendah
        if current_node == goal:
            path_nodes = []
            while current_node is not None:
                path_nodes.insert(0, current_node)
                current_node = path[current_node]
            return path_nodes, path_cost[goal]
        
        # Jika simpul sudah dikunjungi sebelumnya, lewati
        if current_node in visited:
            continue
        
        # Tandai simpul sebagai dikunjungi
        visited.add(current_node)
        
        # Periksa tetangga-tetangga simpul saat ini
        for neighbor, cost in graph[current_node]:
            if neighbor not in visited:
                # Hitung total biaya untuk mencapai tetangga melalui simpul saat ini
                total_cost = current_cost + cost
                
                # Jika total biaya lebih rendah dari yang telah dicatat sebelumnya, perbarui
                if total_cost < path_cost[neighbor]:
                    path_cost[neighbor] = total_cost
                    path[neighbor] = current_node
                    heapq.heappush(priority_queue, (total_cost, neighbor))
    
    # Jika tidak ada jalur yang ditemukan
    return "No path found"

# Contoh graf berbobot
# graph = {
#     'A': [('B', 1), ('C', 4)],
#     'B': [('A', 1), ('C', 2), ('D', 5)],
#     'C': [('A', 4), ('B', 2), ('D', 1)],
#     'D': [('B', 5), ('C', 1)]
# }

graph = {
    'A': [('B', 2), ('C', 3), ('D',5)],
    'B': [('A', 2), ('E', 5),('F',7)],
    'C': [('A', 3), ('E', 1), ('D', 1)],
    'D': [('A', 5), ('C', 1),('E',6)],
    'E': [('C',1),('D',6),('H',3),('G',8),('F',4),('B',5)],
    'F': [('G',2),('E',4),('B',7),('I',5)],
    'G': [('E',6),('F',2)],
    'H': [('D',7),('E',3)],
    'I': [('F',5),('H',4)]
}

start_node = 'A'
goal_node = 'I'

path, cost = ucs(graph, start_node, goal_node)

if path != "No path found":
    print(f"Jalur terpendek dari {start_node} ke {goal_node}: {' -> '.join(path)}")
    print(f"Biaya terendah: {cost}")
else:
    print("Tidak ada jalur yang ditemukan.")
