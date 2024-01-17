import heapq

class Dijkstra:
    def __init__(self):
        self.graph = {}

    def find_shortest_path(self, start_node):
        distances = {node: float('infinity') for node in self.graph}
        distances[start_node] = 0

        priority_queue = [(0, start_node)]

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, edge_weight in self.graph[current_node]:
                distance = current_distance + edge_weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances

    def shortest_path(self, start_node, end_node):
        distances = self.find_shortest_path(start_node)

        path = []
        current_node = end_node

        while current_node != start_node:
            path.insert(0, current_node)
            current_node = min(self.graph[current_node], key=lambda x: distances[x[0]] + x[1])[0]

        path.insert(0, start_node)
        return path

# # Example usage with an adjacency list
# adj_list = {
#     0: [(1, 2)],
#     1: [(0, 2), (2, 1), (3, 7)],
#     2: [(1, 1), (3, 3)],
#     3: [(1, 7), (2, 3)]
# }

# dijkstra = Dijkstra(adj_list)

# shortest_path = dijkstra.shortest_path(0, 3)

# print(f"Shortest Path from 0 to 3: {shortest_path}")