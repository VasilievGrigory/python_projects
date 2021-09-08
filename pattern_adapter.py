class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, grid):
        self.adaptee.set_dim((len(grid[0]), len(grid)))
        self.adaptee.generate_lights()
        lights = obstacles = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 1:
                    lights.append((x, y))
                elif grid[y][x] == -1:
                    obstacles.append((x, y))
        self.adaptee.set_obstacles(obstacles)
        self.adaptee.set_lights(lights)
        ans = self.adaptee.generate_lights()
        return ans
