import heapq

def ucs(graph, start, goal):
    # Inisialisasi antrian prioritas dengan simpul awal dan biaya awal 0
    priority_queue = [(0, start)]
    
    # Inisialisasi set untuk melacak simpul yang sudah dikunjungi
    visited = set()
    
    # Inisialisasi kamus untuk melacak jalur dari simpul awal ke simpul lain
    path = {start: None}
    
    while priority_queue:
        # Ambil simpul dengan biaya terendah dari antrian prioritas
        current_cost, current_node = heapq.heappop(priority_queue)
        
        # Jika sudah mencapai tujuan, kembalikan jalur
        if current_node == goal:
            path_nodes = []
            while current_node is not None:
                path_nodes.insert(0, current_node)
                current_node = path[current_node]
            return path_nodes
        
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
                
                # Jika tetangga belum pernah dikunjungi atau biaya lebih rendah, perbarui jalur dan tambahkan ke antrian
                if neighbor not in path or total_cost < path[neighbor]:
                    path[neighbor] = total_cost
                    heapq.heappush(priority_queue, (total_cost, neighbor))
        
    
    # Jika tidak ada jalur yang ditemukan
    return "No path found"


graph = {
    'A': [('B', 145), ('I', 148), ('X',55),('V',167)],
    'B': [('A', 145), ('C', 98)],
    'C': [('B', 98), ('D', 212)],
    'D': [('K', 102), ('C', 210),('E',102)],
    'E': [('D',102),('L',95),('M',73),('N',97),('F',152),('L',95)],
    'F': [('E',125),('G',83)],
    'G': [('H',75),('F',83)],
    'H': [('G',75)],
    'I': [('A',148),('Q',25),('J',75)],
    'J':[('I',75),('K',95)],
    'K':[('J', 95),('D',102)],
    'L':[('E',95)],
    'M':[('E',73)],
    'N':[('E',97),('O',25),('P',65)],
    'O':[('N',25)],
    'P':[('N',65)],
    'Q':[('X',30),('I',25)],
    'R':[('X',57),('S',93)],
    'S':[('R',93),('T',112)],
    'T':[('S',112),('V',25),('U',75)],
    'U':[('T',75),('V',85)],
    'V':[('U',85),('T',25),('A',167)],
    'X':[('R',57),('Q',25),('A',55)]
    }

def wajib():
    start_node = ['A','H','H','O','I']
    goal_node = ['D','N','U','H','A']

    for i in range(len(goal_node)):
        path, cost = ucs(graph, start_node[i], goal_node[i])

        if path != "No path found":
            print(f"Jalur terpendek dari {start_node[i]} ke {goal_node[i]}: {' -> '.join(path)}")
            print(f"Biaya terendah: {cost}")
        else:
            print("Tidak ada jalur yang ditemukan.")
        print("\n")

print("==== Menu ====")
print("1. Wajib")
print("2. nginput aja dah")
a = int(input("Jawaban anda : "))

if a == 1:
    wajib()
else:
    start = input("Kota Asal : ")
    end = input("Kota Tujuan : ")

    path, cost = ucs(graph, start, end)

    if path != "No path found":
        print(f"Jalur terpendek dari {start} ke {end}: {' -> '.join(path)}")
        print(f"Biaya terendah: {cost}")
    else:
        print("Tidak ada jalur yang ditemukan.")
    print("\n")

