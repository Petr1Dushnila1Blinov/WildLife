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

Light_green = "#f7b5dd"
Ripe_green = "#aa19cf"
Rotten_green = "#ab880c"


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



class Fruit:
    st_growing = 0
    st_ripe = 1
    st_rotten = 2
    st_dead = 3
    Ripe = 500 * 1
    Rotten = 1000 * 1
    Dead = 1500 * 1

    def __init__(self):
        self.coord_x = -10  # x coordinate
        self.coord_y = -10  # y coordinate
        self.age = 0  # возраст куска травы
        self.state = Fruit.st_growing
        self.color = Light_green  # цвет куска травы, зависит от возраста
        self.health = 100  # прочность травы, в общем то, требуемое время на её поедание
        self.saturability = 100  # насыщаемость, как сильно животное наедается куском травы
        self.size = 0  # коэф размера куска травы
        self.id = canv.create_rectangle(self.coord_x - 2 * self.size, self.coord_y + 2 * self.size,
                                        self.coord_x + 2 * self.size, self.coord_y + 2 * self.size,
                                        fill=self.color, outline="#5c1841")
        self.clock = Clock()

    # if fruit is eaten we delete it
    def eaten(self):
        canv.delete(self.id)
        return True

    # defines if lake is nearby
    def lake_nearby(self):
        if ((self.coord_x - x_lake) / (a_axle + 3*self.size)) ** 2 +\
                ((self.coord_y - y_lake) / (b_axle + 3*self.size)) ** 2 <= 1:
            return True
        else:
            return False

    # controls states of fruits and changes it
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

    # updates states
    def update(self):
        self.state_machine()
        self.clock.update()
        if self.state == Fruit.st_dead:
            self.eaten()
        else:
            if self.state == Fruit.st_growing:
                self.size = self.age/Fruit.Ripe * 3
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
                        self.coord_x - 1 * self.size,
                        self.coord_y - 1 * self.size,
                        self.coord_x + 1 * self.size,
                        self.coord_y + 1 * self.size,
                        )
            canv.itemconfig(self.id,
                            fill=self.color)
