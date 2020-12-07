import math
from Landscape import *
# needed parameters for cattle

@contract
def lake_force(mass, x_coord, y_coord):
    """
            :param mass - float, >0, масса
            :param x_coord - float, собственная координата x
            :param y_coord - float, собственная координата y
    """
    r = math.sqrt((x_coord - x_lake) ** 2 + (y_coord - y_lake) ** 2)
    force_x = mass * M / r ** 2 * (x_coord - x_lake) / r
    force_y = mass * M / r ** 2 * (y_coord - y_lake) / r
    return force_x, force_y


@contract
def obj_force(obj, mass, x_coord, y_coord, x_obj, y_obj, MASS):
    """
            :param obj - объект
            :param mass - float, >0, масса
            :param x_coord - float, собственная координата x
            :param y_coord - float, собственная координата y
            :param x_obj - float, координата x объекта
            :param y_obj - float, координата y объекта
            :param MASS - float, >0, масса объекта
    """
    r = math.sqrt((x_coord - x_obj) ** 2 + (y_coord - y_obj) ** 2)
    force_x = mass * MASS / r ** 2 * (x_coord - x_obj) / r
    force_y = mass * MASS / r ** 2 * (y_coord - y_obj) / r
    return force_x, force_y


# needed parameters for cattle
class Cattle:
    def __init__(self):
        self.coord_x = 1  # x coordinate
        self.coord_y = 1  # y coordinate
        self.velocity_x = 1  # speed x-axis
        self.velocity_y = 1  # speed y-axis
        self.hunger = 0  # represents how hungry the animal is
        self.thirst = 0  # represents how thirsty the animal is
        self.health = 100  # represents the health points
        self.anxiety = 0  # represents how anxious the animal is
        self.mass = 10**3  # mass of the animal
        self.radius = 1  # radius of image
        self.color = 'green'
        # creates the image of an animal
        self.id = canv.create_oval(self.coord_x - self.radius,
                                    self.coord_y - self.radius,
                                    self.coord_x + self.radius,
                                    self.coord_y + self.radius,
                                    fill=self.color)

    def move(self):
        canv.coords(self.id,
                    self.coord_x - self.radius + self.velocity_x,
                    self.coord_y - self.radius + self.velocity_y,
                    self.coord_x + self.radius + self.velocity_x,
                    self.coord_y + self.radius + self.velocity_y)

    def death(self):
        if self.health == 0:
            canv.delete(self.id)

    def lake_force(self):
        lake_force(self.mass, self.coord_x, self.coord_y)

    def obj_force(self, obj):
        obj_force(obj, self.mass, self.coord_x, self.coord_y, obj.coord_x, obj.coord_y, obj.mass)


class Predator:
    def __init__(self):
        self.coord_x = 1  # x coordinate
        self.coord_y = 1  # y coordinate
        self.velocity_x = 2  # speed x-axis
        self.velocity_y = 1  # speed y-axis
        self.hunger = 0  # represents how hungry the animal is
        self.thirst = 0  # represents how thirsty the animal is
        self.health = 100  # represents the health points
        self.mass = 10**3  # mass of the animal
        self.radius = 1  # radius of image
        self.color = 'red'
        # creates the image of an animal
        self.id = canv.create_oval(self.coord_x - self.radius,
                                    self.coord_y - self.radius,
                                    self.coord_x + self.radius,
                                    self.coord_y + self.radius,
                                    fill=self.color)

    def move(self):
        canv.coords(self.id,
                    self.coord_x - self.radius + self.velocity_x,
                    self.coord_y - self.radius + self.velocity_y,
                    self.coord_x + self.radius + self.velocity_x,
                    self.coord_y + self.radius + self.velocity_y)

    def lake_force(self):
        lake_force(self.mass, self.coord_x, self.coord_y)

    def obj_force(self, obj):
        obj_force(obj, self.mass, self.coord_x, self.coord_y, obj.coord_x, obj.coord_y, obj.mass)


