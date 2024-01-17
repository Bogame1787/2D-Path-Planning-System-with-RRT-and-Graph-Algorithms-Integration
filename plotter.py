import pygame

import env
import sys

class Plotter:
    def __init__(self, env, vertex, adj, paths):
        pygame.init()

        self.WIDTH, self.HEIGHT = 800, 800
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.DARK_BLUE = (0, 0, 100)
        self.DARK_GREEN = (0, 200, 0)
        self.DARK_RED = (200, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.PINK = (255, 192, 203)
        self.GREY = (32, 32, 32)
        self.FPS = 60

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Plotter Example")
        self.clock = pygame.time.Clock()

        self.shapes = []

        self.vertex = vertex
        self.adj = adj
        self.paths = paths
        self.path_colors = [self.YELLOW, self.PINK]

        for rect in env.obs_rectangle:
            self.add_rectangle(*rect)

        # for bound in env.obs_boundary:
        #     self.add_rectangle(*bound)

        for circle in env.obs_circle:
            self.add_circle(*circle)    

    def add_rectangle(self, x, y, width, height):
        self.shapes.append(('rectangle', x, y, width, height))

    def add_circle(self, x, y, radius):
        self.shapes.append(('circle', x, y, radius))

    def draw(self):
        for shape in self.shapes:
            if shape[0] == 'rectangle':
                pygame.draw.rect(self.screen, self.GREY, pygame.Rect(shape[1:]))
            elif shape[0] == 'circle':
                pygame.draw.circle(self.screen, self.GREY, (shape[1], shape[2]), shape[3])

        for node in self.adj:
            for neighbour in self.adj[node]:
                pygame.draw.line(self.screen, self.DARK_RED, (self.vertex[node].x, self.vertex[node].y), (self.vertex[neighbour[0]].x, self.vertex[neighbour[0]].y), 2)
        
        if self.paths:
            for idx, path in enumerate(self.paths):
                for i in range(len(path) - 1):
                    pygame.draw.line(self.screen, self.path_colors[idx], (self.vertex[path[i]].x, self.vertex[path[i]].y), (self.vertex[path[i+1]].x, self.vertex[path[i+1]].y), 5)


        for node in self.vertex:
            pygame.draw.circle(self.screen, self.DARK_GREEN, (node.x, node.y), 4)


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # mouse_x, mouse_y = pygame.mouse.get_pos()

            # print(mouse_x, mouse_y)
            self.screen.fill(self.DARK_BLUE)

            self.draw()

            pygame.display.flip()

            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    envi = env.Env()
    plotter = Plotter(envi, [], {})

    plotter.run()

