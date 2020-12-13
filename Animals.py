import math

# from contracts import contract

from Landscape import *


def lake_force(mass, x_coord, y_coord):
    """
            :param mass float, >0, масса зверя
            :param x_coord float, собственная координата x
            :param y_coord float, собственная координата y
    """
    r = math.sqrt((x_coord - x_lake) ** 2 + (y_coord - y_lake) ** 2)
    force_x = mass * M / r ** 2 * (x_coord - x_lake) / r
    force_y = mass * M / r ** 2 * (y_coord - y_lake) / r
    return force_x, force_y


def obj_force(obj, mass, x_coord, y_coord, x_obj, y_obj, MASS):
    """
            :param obj объект
            :param mass float, >0, масса
            :param x_coord float, собственная координата x
            :param y_coord float, собственная координата y
            :param x_obj float, координата x объекта
            :param y_obj float, координата y объекта
            :param MASS float, >0, масса объекта
    """
    r = math.sqrt((x_coord - x_obj) ** 2 + (y_coord - y_obj) ** 2)
    force_x = mass * MASS / r ** 2 * (x_coord - x_obj) / r
    force_y = mass * MASS / r ** 2 * (y_coord - y_obj) / r
    return force_x, force_y


class Clock:
    def __init__(self):
        self.is_running = False
        self.stop_time = 0

    def start(self, period):
        self.is_running = True
        self.stop_time = time.time() + period

    def update(self):
        if time.time() > self.stop_time:
            self.is_running = False


class Animal:
    def __init__(self):
        self.coord_x = 1  # x coordinate
        self.coord_y = 1  # y coordinate
        self.velocity_x = 0  # speed x-axis
        self.velocity_y = 0  # speed y-axis
        self.hunger = 0  # represents how hungry the animal is
        self.thirst = 0  # represents how thirsty the animal is
        self.health = 100  # represents the health points
        self.mass = 10 ** 3  # mass of the animal
        self.radius = 10  # radius of image
        self.color = 'green'
        # creates the image of an animal

    def move(self, delta_t):
        self.coord_x += self.velocity_x * delta_t
        self.coord_y += self.velocity_y * delta_t
        if self.coord_x < self.radius:
            self.velocity_x *= -1
            self.coord_x += self.velocity_x * delta_t
        if self.coord_x > length-self.radius:
            self.velocity_x *= -1
            self.coord_x += self.velocity_x * delta_t
        if self.coord_y < self.radius:
            self.velocity_y *= -1
            self.coord_x += self.velocity_x * delta_t
        if self.coord_y > height-self.radius:
            self.velocity_y *= -1
            self.coord_x += self.velocity_x * delta_t
        canv.coords(self.id,
                    self.coord_x - self.radius,
                    self.coord_y - self.radius,
                    self.coord_x + self.radius,
                    self.coord_y + self.radius)

    def update(self):
        pass

    def lake_force(self):
        return self.thirst * lake_force(self.mass, self.coord_x, self.coord_y)


# needed parameters for cattle
class Cattle(Animal):
    def __init__(self):
        Animal.__init__(self)
        self.anxiety = 0  # represents how anxious the animal is
        self.mass = 10 ** 3  # mass of the animal
        self.color = 'green'
        self.notice_radius = 20
        self.id = canv.create_oval(self.coord_x - self.radius,
                                   self.coord_y - self.radius,
                                   self.coord_x + self.radius,
                                   self.coord_y + self.radius,
                                   fill=self.color)
        self.clock = Clock()

    def death(self):
        if self.health <= 0:
            canv.delete(self.id)
            return True

    def update(self):
        V = 30  # Скорость движения жертв
        self.clock.update()
        if not self.clock.is_running:
            self.velocity_x = randint(-V, V)
            self.velocity_y = randint(-V, V)
            self.clock.start(2)


class Predator(Animal):
    st_idle = 0
    st_chase = 1
    st_thirst = 2
    st_drink = 3
    st_dead = 4

    def death(self):
        if self.health <= 0:
            canv.delete(self.id)
            return True

    def notice_cattle(self):
        if self.nearest_cattle == None:
            return False
        r = math.sqrt((self.nearest_cattle.coord_x - self.coord_x) ** 2 +
                      (self.nearest_cattle.coord_y - self.coord_y) ** 2)
        if r <= self.notice_radius:
            return True
        else:
            return False

    def is_thirsty(self):
        pass  # FIXME: хочет пить?

    def lake_nearby(self):
        pass  # FIXME: озеро рядом?

    def state_machine(self):

        if self.health < 0:
            self.state = Predator.st_dead
        else:
            if self.state == Predator.st_idle and self.notice_cattle():
                self.state = Predator.st_chase
            if self.state == Predator.st_chase and not self.notice_cattle():
                self.state = Predator.st_idle
            if self.state == Predator.st_idle and self.is_thirsty():
                self.state = Predator.st_thirst
            if self.state == Predator.st_chase and self.is_thirsty():
                self.state = Predator.st_thirst
            if self.state == Predator.st_thirst and self.lake_nearby():
                self.state = Predator.st_drink
            if not self.is_thirsty() and self.state >= Predator.st_thirst:
                self.state = Predator.st_idle

    def __init__(self):
        Animal.__init__(self)
        self.color = 'red'
        self.mass = 10 ** 2
        self.notice_radius = 300
        self.state = Predator.st_idle
        self.nearest_cattle = None
        self.health = 30
        self.velocity = 10  # Скорость передвижения хищников
        self.id = canv.create_oval(self.coord_x - self.radius,
                                   self.coord_y - self.radius,
                                   self.coord_x + self.radius,
                                   self.coord_y + self.radius,
                                   fill=self.color)
        self.clock = Clock()

    def update(self):
        self.state_machine()
        self.clock.update()
        if self.state == Predator.st_dead:
            self.death()
        else:
            if self.state == Predator.st_idle and not self.clock.is_running:
                varphi = randint(-180, 180)
                self.velocity_x = self.velocity * math.cos(varphi)
                self.velocity_y = self.velocity * math.sin(varphi)
                self.clock.start(2)
                self.health -= 10

            if self.state == Predator.st_chase:
                d_x = (- self.coord_x + self.nearest_cattle.coord_x)
                d_y = (- self.coord_y + self.nearest_cattle.coord_y)
                r = math.sqrt(d_x ** 2 + d_y ** 2)
                if r < self.radius:
                    self.nearest_cattle.health -= 10
                if r > 0:
                    self.velocity_x = self.velocity * d_x / r
                    self.velocity_y = self.velocity * d_y / r

    def obj_force(self, obj):
        return self.hunger * obj_force(obj, self.mass, self.coord_x, self.coord_y, obj.coord_x, obj.coord_y, obj.mass)
