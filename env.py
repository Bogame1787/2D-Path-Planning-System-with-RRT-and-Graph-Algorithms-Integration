class Env:
    def __init__(self):
        self.x_range = (0, 800)
        self.y_range = (0, 800)
        self.obs_boundary = self.obs_boundary()
        self.obs_circle = self.obs_circle()
        self.obs_rectangle = self.obs_rectangle()

        # self.obs_boundary = []
        # self.obs_circle = []
        # self.obs_rectangle = []

    def obs_boundary(self):
        obs_boundary = [
            [0, 0, 10, 800],
            [0, 800, 800, 10],
            [10, 0, 800, 10],
            [800, 10, 10, 800]
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [300, 350, 160, 100],
            [600, 600, 100, 100],
            [100, 500, 100, 150],
            [500, 140, 100, 100]
        ]
        return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [
            [100, 120, 60],
            [700, 200, 60],
            [250, 250, 50],
            [370, 70, 30],
            [370, 550, 70]
        ]

        return obs_cir