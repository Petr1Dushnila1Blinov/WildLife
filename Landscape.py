from random import *
import tkinter as tk
from Clock import *
from PIL import Image, ImageTk

root = tk.Tk()
fr = tk.Frame(root)
length = 800
height = 600
root.geometry(str(length) + 'x' + str(height))
canv = tk.Canvas(root, bg='#fb0')
image = Image.open("gameground.png")
photo = ImageTk.PhotoImage(image)
image = canv.create_image(0, 0, anchor='nw', image=photo)
canv.pack(fill=tk.BOTH, expand=1)

global GO_MAIN
GO_MAIN = False

Light_green = "#09e31f"
Ripe_green = "#138f1f"
Rotten_green = "#839e39"


# creates lake
def lake(canv):
    """
    :param canv: canvas
    :return: x_lake - lake x coord, y_lake - lake y coord, a - big axle, b - small axle
    """
    a = randint(20, 120)  # big axle
    b = randint(20, 120)  # small axle
    x_lake = randint(0, length)  # lake x coord
    y_lake = randint(0, height)  # lake y coord
    canv.create_oval(
        x_lake - a, y_lake - b, x_lake + a, y_lake + b, outline="gold",
        fill="deep sky blue", width=4
    )
    return x_lake, y_lake, a, b


(x_lake, y_lake, a_axle, b_axle) = lake(canv)

'''
def draw_grass(x, y, size, color, canv):
    canv.create_arc(x - 5 * size, y - 5 * size, x + 5 * size, y + 5 * size, start=0,
                    extent=180, fill=color, width=0.2)
    for i in range(0, 45):
        for j in range(-4, 5):
            canv.create_line(x + (j / 5) * i / 10 * size, y + (i / 10) ** 2 * size,
                             x + (j / 5) * (i + 1) / 10 * size, y + ((i + 1) / 10) ** 2 * size, fill=color)
'''


class Fruit:
    st_growing = 0
    st_ripe = 1
    st_rotten = 2
    st_dead = 3
    Ripe = 500
    Rotten = 1000
    Dead = 1500

    def __init__(self):
        self.coord_x = -10  # x coordinate
        self.coord_y = -10  # y coordinate
        self.age = 0  # возраст куска травы
        self.state = Fruit.st_growing
        self.color = Light_green  # цвет куска травы, зависит от возраста
        self.health = 100  # прочность травы, в общем то, требуемое время на её поедание
        self.saturability = 100  # насыщаемость, как сильно животное наедается куском травы
        self.size = 2  # коэф размера куска травы
        self.id = canv.create_rectangle(self.coord_x - 2 * self.size, self.coord_y + 2 * self.size,
                                        self.coord_x + 2 * self.size, self.coord_y + 2 * self.size,
                                        fill=self.color, outline="gold")
        self.clock = Clock()

    def eaten(self):
        canv.delete(self.id)
        return True

    def lake_nearby(self):
        if ((self.coord_x - x_lake) / (a_axle + 3*self.size)) ** 2 +\
                ((self.coord_y - y_lake) / (b_axle + 3*self.size)) ** 2 <= 1:
            return True
        else:
            return False

    # def being_eaten(self):

    def state_machine(self):
        if (self.health < 0) or self.age >= Fruit.Dead:
            self.state = Fruit.st_dead
        else:
            if self.age < Fruit.Ripe:
                self.state = Fruit.st_growing
            if Fruit.Ripe <= self.age < Fruit.Rotten:
                self.state = Fruit.st_ripe
            if self.age >= Fruit.Rotten:
                self.state = Fruit.st_rotten
            if self.lake_nearby() is True:
                self.state = Fruit.st_dead

    def update(self):
        self.state_machine()
        self.clock.update()
        if self.state == Fruit.st_dead:
            self.eaten()
        else:
            if self.state == Fruit.st_growing:
                self.color = Light_green
            elif self.state == Fruit.st_ripe:
                self.saturability -= (self.age - Fruit.Rotten) * 10
                self.color = Ripe_green
            elif self.state == Fruit.st_rotten:
                self.saturability -= (self.age - Fruit.Rotten)
                self.color = Rotten_green

            self.clock.start(0.1)
            self.age += 1
            canv.coords(self.id,
                        self.coord_x - 2 * self.size,
                        self.coord_y - 2 * self.size,
                        self.coord_x + 2 * self.size,
                        self.coord_y + 2 * self.size,
                        )
            canv.itemconfig(self.id,
                            fill=self.color)
