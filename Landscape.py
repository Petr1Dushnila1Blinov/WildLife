from random import *
import tkinter as tk
from Clock import *

root = tk.Tk()
fr = tk.Frame(root)
length = 800
height = 600
root.geometry(str(length) + 'x' + str(height))
canv = tk.Canvas(root, bg='#fb0')
canv.create_rectangle(
    0, 0, length, height,
    outline="lime green", fill="lime green")
canv.pack(fill=tk.BOTH, expand=1)
global GO_MAIN
GO_MAIN = False

Light_green = (9, 227, 31)
Ripe_green = (19, 143, 31)
Rotten_green = (131, 158, 57)


# creates lake
def lake(canv):
    """
    :param canv: canvas
    :return: x_lake - lake x coord, y_lake - lake y coord, a - big axle, b - small axle
    """
    a = randint(20, 120)  # big axle
    b = randint(20, 120)  # small axle
    x_lake = randint(0, height)  # lake x coord
    y_lake = randint(0, length)  # lake y coord
    canv.create_oval(
        x_lake - a, y_lake - b, x_lake + a, y_lake + b, outline="gold",
        fill="deep sky blue", width=4
    )
    return x_lake, y_lake, a, b


(x_lake, y_lake, a_axle, b_axle) = lake(canv)


def draw_grass(x, y, size, color):
    canv.create_arc(x - 5 * size, y - 5 * size, x + 5 * size, y + 5 * size, start=0,
                    extent=180, fill=color, width=0.2)
    for i in range(0, 45):
        for j in range(-4, 5):
            canv.create_line(x + (j / 5) * i / 10 * size, y + (i / 10) ** 2 * size,
                             x + (j / 5) * (i + 1) / 10 * size, y + ((i + 1) / 10) ** 2 * size, fill=color)


class Grass:
    st_growing = 0
    st_ripe = 1
    st_rotten = 2
    st_dead = 3
    Ripe = 10
    Rotten = 17
    Dead = 25
    def __init__(self):
        self.coord_x = -10  # x coordinate
        self.coord_y = -10  # y coordinate
        self.age = 0  # возраст куска травы
        self.state = st_growing
        self.color = Light_green  # цвет куска травы, зависит от возраста
        self.health = 100  # прочность травы, в общем то, требуемое время на её поедание
        self.saturability = 100  # насыщаемость, как сильно животное наедается куском травы
        self.size = 1  # коэф размера куска травы
        self.id = draw_grass(self.coord_x, self.coord_y, self.color)
        self.clock = Clock()

    def eaten(self):
        canv.delete(self.id)
        return True

    def lake_nearby(self):
        if ((self.coord_x - x_lake) / (a_axle + R)) ** 2 + ((self.coord_y - y_lake) / (b_axle + R)) ** 2 <= 1:
            return True
        else:
            return False

    #def being_eaten(self):

    def state_machine(self):
        if (self.health < 0) or self.age >= Grass.Dead:
            self.state = Grass.st_dead
        else:
            if self.age < Grass.Ripe:
                self.state = Grass.st_growing
            if Grass.Ripe <= self.age < Grass.Rotten:
                self.state = Grass.st_ripe
            if self.age >= Grass.Rotten:
                self.state = Grass.st_rotten


    def update(self):
        self.state_machine()
        self.clock.update()
        if self.state == Grass.st_dead:
            self.eaten()
        else:
            if self.state == Grass.st_growing:
                self.clock.start(100)
                self.color = Light_green
                self.age += 1
            elif self.state == Grass.st_ripe:
                self.saturability -= (self.age - Rotten)*10
                self.color = Ripe_green
                self.clock.start(100)
                self.age += 1
            elif self.state == Grass.st_rotten:
                self.saturability -= (self.age - Rotten)
                self.color = Rotten_green
                self.clock.start(100)
                self.age += 1






