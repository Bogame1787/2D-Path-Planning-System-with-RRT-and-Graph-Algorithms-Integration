import heapq

class A_Star:
    def __init__(self):
        self.graph = {}

    def add_edge(self, node1, node2, cost):
        if node1 not in self.graph:
            self.graph[node1] = []
        self.graph[node1].append((node2, cost))

    def heuristic(self, node, goal):
        return abs(node - goal)

    def shortest_path(self, start, goal):
        open_set = []
        closed_set = set()
        heapq.heappush(open_set, (0, start, []))

        while open_set:
            current_cost, current_node, path = heapq.heappop(open_set)

            if current_node in closed_set:
                continue

            path = path + [current_node]

            if current_node == goal:
                return path

            closed_set.add(current_node)

            if current_node not in self.graph:
                continue

            for neighbor, cost in self.graph[current_node]:
                if neighbor not in closed_set:
                    total_cost = current_cost + cost
                    priority = total_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, neighbor, path))

        return None

# # Example usage:
# # Create a graph
# my_graph = Graph()
# my_graph.add_edge(1, 2, 1)
# my_graph.add_edge(1, 3, 2)
# my_graph.add_edge(2, 4, 3)
# my_graph.add_edge(2, 5, 1)
# my_graph.add_edge(3, 6, 2)
# my_graph.add_edge(3, 7, 1)

# # Find the shortest path from node 1 to node 7 using A*
# start_node = 1
# end_node = 7
# path = my_graph.a_star(start_node, end_node)

# print(my_graph.graph)
# if path:
#     print(f"Shortest path from {start_node} to {end_node}: {path}")
# else:
#     print(f"No path found from {start_node} to {end_node}")
