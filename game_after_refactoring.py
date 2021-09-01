import math
import random
import pygame
import os

SCREEN_DIM = (800, 600)

class Vec2d:


    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def __add__(self, other):
        return Vec2d((self.x + other.x, self.y + other.y))


    def __sub__(self, other):
        return Vec2d((self.x - other.x, self.y - other.y))

    def __mul__(self, val):
        return Vec2d((self.x * val, self.y * val))

    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        return self.x, self.y


class Polyline:


    def __init__(self, points=[], speeds=[]):
        self.points = points
        self.speeds = speeds

    def append_new_point(
            self,
            point,
            speed=(random.random() * 2, random.random() * 2)
    ):
        self.points.append(Vec2d(point))
        self.speeds.append(Vec2d(speed))

    def set_points(self):
        """функция перерасчета координат опорных точек"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d((- self.speeds[p].x, self.speeds[p].y))
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d((self.speeds[p].x, -self.speeds[p].y))

    def draw_points(self, points=None, style="points", width=3, color=(255, 255, 255), gameDisplay=None):
        """функция отрисовки точек на экране"""
        if gameDisplay == None:
            return
        points = points if points!=None else self.points
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(p.x), int(p.y)), width)

    def restart(self):
        self.points = []
        self.speeds = []


class Knot(Polyline):


    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        res = []
        for i in range(count):
            res.append(self.get_point(points=base_points, alpha=i * (1 / count)))
        return res

    def get_knot(self, count=35):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn, count))
        return res


class Game:


    __count = 0
    __working = True
    __pause = True
    __show_help = False

    def __new__(cls, *args, **kwargs):
        if cls.__count == 0:
            return super().__new__(cls)

    def __init__(self, steps=35):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode(SCREEN_DIM)
        self.steps = steps
        self.hue = 0
        self.color = pygame.Color(0)
        self.__player_knot = Knot()
        pygame.display.set_caption("MyScreenSaver")

    def play_game(self):
        while self.__working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__working = False
                    if event.key == pygame.K_r:
                        self.__player_knot.restart()
                    if event.key == pygame.K_p:
                        self.__pause = not self.__pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                    if event.key == pygame.K_F1:
                        self.__show_help = not self.__show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__player_knot.append_new_point(event.pos)

            self.gameDisplay.fill((0, 0, 0))
            self.hue = (self.hue + 1) % 360
            self.color.hsla = (self.hue, 100, 50, 100)
            self.__player_knot.draw_points(gameDisplay=self.gameDisplay)
            self.__player_knot.draw_points(
                self.__player_knot.get_knot(self.steps), style="line", width=3, color=self.color, gameDisplay=self.gameDisplay)
            if not self.__pause:
                self.__player_knot.set_points()
            if self.__show_help:
                self.draw_help()

            pygame.display.flip()

    def draw_help(self):
        """функция отрисовки экрана справки программы"""
        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = []
        data.append(["F1", "Show Help"])
        data.append(["R", "Restart"])
        data.append(["P", "Pause/Play"])
        data.append(["Num+", "More points"])
        data.append(["Num-", "Less points"])
        data.append(["", ""])
        data.append([str(self.steps), "Current points"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

    def __del__(self):
        pygame.display.quit()
        pygame.quit()



def main():
    game = Game()
    game.play_game()


if __name__ == '__main__':
    main()

