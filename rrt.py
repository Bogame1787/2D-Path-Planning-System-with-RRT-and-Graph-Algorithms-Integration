import os
import sys
import math
import numpy as np

import env
import plotter
import utils

from dijikstra import Dijkstra
from a_star import A_Star
from node import Node
# np.random.seed(128)


class RRT:
    def __init__(self, s_start, step_len, thresh, goal_sample_rate, iter_max):
        self.s_start = Node(s_start)
        self.s_start.id = 0

        self.step_len = step_len
        self.goal_sample_rate = goal_sample_rate
        self.iter_max = iter_max
        self.thresh = thresh

        self.vertex = [self.s_start]
        self.adj = {0:[]}
        self.coord_id = {(self.s_start.x, self.s_start.y):0}
        self.env = env.Env()
        self.utils = utils.Utils()

        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.obs_boundary = self.env.obs_boundary

    def planning(self):
        k = 1
        for _ in range(self.iter_max):
            node_rand = self.generate_random_node(self.goal_sample_rate)
            node_near = self.nearest_neighbor(self.vertex, node_rand)
            node_new = self.new_state(node_near, node_rand)

            if node_new and not self.utils.is_collision(node_near, node_new):
                node_new.id = k
                dist, _ = self.get_distance_and_angle(node_new, node_new.parent)

                self.adj[k] = [(node_new.parent.id, dist)]
                self.adj[node_new.parent.id].append((k, dist))
                self.vertex.append(node_new)
                neighbours = self.get_neighbours(node_new)
                for neighbour in neighbours:
                    if neighbour.id != node_new.parent.id:
                        dist, _ = self.get_distance_and_angle(node_new, node_new.parent)

                        self.adj[k].append((neighbour.id, dist))
                        self.adj[neighbour.id].append((k, dist))
                k+=1

        return None

    def get_neighbours(self, node_new):
        neighbours = []
        for node in self.vertex:
            dist, _ = self.get_distance_and_angle(node_new, node)
            if dist > 0 and dist < self.thresh:
                neighbours.append(node)
        
        return neighbours


    def generate_random_node(self, goal_sample_rate):
        delta = self.utils.delta

        if np.random.random() > goal_sample_rate:
            return Node((np.random.uniform(self.x_range[0] + delta, self.x_range[1] - delta),
                         np.random.uniform(self.y_range[0] + delta, self.y_range[1] - delta)))

        return self.s_goal

    @staticmethod
    def nearest_neighbor(node_list, n):
        return node_list[int(np.argmin([math.hypot(nd.x - n.x, nd.y - n.y)
                                        for nd in node_list]))]

    def new_state(self, node_start, node_end):
        dist, theta = self.get_distance_and_angle(node_start, node_end)

        dist = max(min(self.step_len[1], dist), self.step_len[0])
        node_new = Node((node_start.x + dist * math.cos(theta),
                         node_start.y + dist * math.sin(theta)))
        node_new.parent = node_start

        return node_new

    def extract_path(self, node_end):
        path = [(self.s_goal.x, self.s_goal.y)]
        node_now = node_end

        while node_now.parent is not None:
            node_now = node_now.parent
            path.append((node_now.x, node_now.y))

        return path

    @staticmethod
    def get_distance_and_angle(node_start, node_end):
        dx = node_end.x - node_start.x
        dy = node_end.y - node_start.y
        return math.hypot(dx, dy), math.atan2(dy, dx)


def main():
    x_start = (20, 20)

    rrt = RRT(x_start, [20, 25], 26, 0.0, 1500)
    path = rrt.planning()

    # print(rrt.vertex)
    # print(rrt.adj)

    graph = rrt.adj

    path_finders = [A_Star(), Dijkstra()]

    for path_finder in path_finders:
        path_finder.graph = graph

    
    start_node = 0
    end_node = 500

    paths = [path_finder.shortest_path(start_node, end_node) for path_finder in path_finders]

    # print(path)

    for path in paths:
        print(path)

    # for k in path:
    #     print(rrt.vertex[k].x, rrt.vertex[k].y)

    plotting = plotter.Plotter(rrt.env, rrt.vertex, rrt.adj, paths)
    plotting.run()

if __name__ == '__main__':
    main()
