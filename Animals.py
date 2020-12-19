import math
import time

global R, length, height
R = 10
length, height = 800, 600
from Landscape import *
from Clock import *


class Animal:
    def __init__(self):
        self.coord_x = -10  # x coordinate
        self.coord_y = -10  # y coordinate
        self.velocity_x = 0  # speed x-axis
        self.velocity_y = 0  # speed y-axis
        self.hunger = 0  # represents how hungry the animal is
        self.thirst = randint(0, 30000)  # represents how thirsty the animal is
        self.health = 10000  # represents the health points
        self.mass = 10 ** 3  # mass of the animal
        self.radius = R  # radius of image
        self.color = 'green'
        # creates the image of an animal

    # allows animals to move around
    def move(self, delta_t):
        """
        :param delta_t: update time
        """
        self.coord_x += self.velocity_x * delta_t
        self.coord_y += self.velocity_y * delta_t
        # controls if animals are inside the map
        if self.coord_x <= self.radius:
            self.velocity_x *= -1
            self.coord_x += self.velocity_x * delta_t
        if self.coord_x >= length - self.radius:
            self.velocity_x *= -1
            self.coord_x += self.velocity_x * delta_t
        if self.coord_y <= self.radius:
            self.velocity_y *= -1
            self.coord_y += self.velocity_y * delta_t
        if self.coord_y >= height - self.radius:
            self.velocity_y *= -1
            self.coord_y += self.velocity_y * delta_t
        # controls if animals can enter lake surface
        if ((x_lake - self.coord_x) / (a_axle + self.radius)) ** 2 + (
                (y_lake - self.coord_y) / (b_axle + self.radius)) ** 2 <= 1:
            self.velocity_y *= -1
            self.velocity_x *= -1
            self.coord_x += abs(random()) * self.velocity_x * delta_t
            self.coord_y += abs(random()) * self.velocity_y * delta_t
        canv.coords(self.id,
                    self.coord_x - self.radius,
                    self.coord_y - self.radius,
                    self.coord_x + self.radius,
                    self.coord_y + self.radius)


# needed parameters for cattle(peaceful animals)
class Cattle(Animal):
    st_hungry = -1 # always wanna eat
    st_idle = 0  # wandering around state
    st_runaway = 1  # run_away from predator
    st_thirst = 2  # thirsty state
    st_drink = 3  # drinking state
    st_dead = 4  # dead state

    def __init__(self):
        Animal.__init__(self)
        self.anxiety = 0  # represents how anxious the animal is
        self.state = Cattle.st_idle
        self.nearest_predator = None  # if cattle could identify predator near it
        self.nearest_fruit = None  # if cattle could identify predator near it
        self.velocity = 35  # cattle basic speed
        self.color = 'green'
        self.birfability = 0
        self.eaten = 0
        self.under_attack = False
        self.notice_radius = 40  # radius where cattle notices objects
        self.id = canv.create_oval(self.coord_x - self.radius,
                                   self.coord_y - self.radius,
                                   self.coord_x + self.radius,
                                   self.coord_y + self.radius,
                                   fill=self.color)
        self.clock = Clock()

    def death(self):
        if self.health < 0:
            canv.delete(self.id)
            return True

    # function that defines nearest predator
    def notice_predator(self):
        if self.nearest_predator == None:
            return False
        else:
            r = math.sqrt((self.nearest_predator.coord_x - self.coord_x) ** 2 +
                          (self.nearest_predator.coord_y - self.coord_y) ** 2)
            if r <= self.notice_radius:
                return True
            else:
                return False

    # function that controls state of thirst
    def is_thirsty(self):
        if (self.thirst > 50000 and self.state != 3) or (self.thirst > -50000 and self.state == 3):
            self.health -= 1
            return True
        else:
            return False

    # function that identifies if there is lake near cattle
    def lake_nearby(self):
        if ((self.coord_x - x_lake) / (a_axle + R)) ** 2 + ((self.coord_y - y_lake) / (b_axle + R)) ** 2 <= 1:
            return True
        else:
            return False

    # function that updates parametres after eating
    def eat(self, object):
        if object.state is not Fruit.st_dead and object.state is not Fruit.st_growing:
            self.hunger -= object.saturability
            self.birfability += int(object.saturability / 10)
            self.health += 20
            self.thirst += 4
            self.nearest_fruit.health -= 200
            self.clock.start(200)


    # function that defines nearest fruit
    def notice_fruit(self):
        if self.nearest_fruit == None:
            return False
        elif self.nearest_fruit.state is self.nearest_fruit.st_ripe\
                or self.nearest_fruit.state is self.nearest_fruit.st_rotten:
            r = math.sqrt((self.nearest_fruit.coord_x - self.coord_x) ** 2 +
                          (self.nearest_fruit.coord_y - self.coord_y) ** 2)
            if r <= self.notice_radius:
                return True
            else:
                return False
        else:
            return False

    # controls states and changes it
    def state_machine(self):
        if (self.health < 0) or (self.hunger > 100000):
            self.state = Cattle.st_dead
        else:
            if self.state == Cattle.st_idle and self.notice_predator():
                self.state = Cattle.st_runaway
            if self.state == Cattle.st_runaway and not self.notice_predator():
                self.state = Cattle.st_idle
            if self.state == Cattle.st_idle and self.is_thirsty():
                self.state = Cattle.st_thirst
            if self.state == Cattle.st_thirst and self.lake_nearby():
                self.state = Cattle.st_drink
            if not self.is_thirsty() and self.state >= Cattle.st_thirst:
                self.state = Cattle.st_idle
            if self.state == Cattle.st_idle and not self.is_thirsty() and self.notice_fruit():
                self.state = Cattle.st_hungry

    # makes world moving
    def update(self):
        self.state_machine()
        self.clock.update()
        if self.state == Cattle.st_dead:
            self.death()
        else:
            if self.state == Cattle.st_idle and not self.clock.is_running:
                varphi = randint(-180, 180)
                self.velocity_x = self.velocity * math.cos(varphi)
                self.velocity_y = self.velocity * math.sin(varphi)
                self.clock.start(2)
                self.thirst += 2000


            if self.state == Cattle.st_runaway:
                d_x = (- self.coord_x + self.nearest_predator.coord_x)
                d_y = (- self.coord_y + self.nearest_predator.coord_y)
                r = math.sqrt(d_x ** 2 + d_y ** 2)
                self.velocity_x = -self.velocity * d_x / r
                self.velocity_y = -self.velocity * d_y / r
                self.hunger += 2
                self.thirst += 2

            if self.state == Cattle.st_thirst:
                d_x = (- self.coord_x + x_lake)
                d_y = (- self.coord_y + y_lake)
                r = math.sqrt(d_x ** 2 + d_y ** 2)
                self.velocity_x = self.velocity * d_x / r
                self.velocity_y = self.velocity * d_y / r
                self.hunger += 3

            if self.state == Cattle.st_drink:
                self.velocity_x = 0
                self.velocity_y = 0
                self.clock.start(2)
                self.thirst -= 80
                self.health = 40000

            if self.state == Cattle.st_hungry and self.notice_fruit() is True:
                d_x = (- self.coord_x + self.nearest_fruit.coord_x)
                d_y = (- self.coord_y + self.nearest_fruit.coord_y)
                r = math.sqrt(d_x ** 2 + d_y ** 2)
                if r < self.radius:
                    self.eat(self.nearest_fruit)
                else:
                    self.velocity_x = self.velocity * d_x / r
                    self.velocity_y = self.velocity * d_y / r
                    self.thirst += 2
                    self.hunger += 1


class Predator(Animal):
    st_idle = 0  # wandering around state
    st_chase = 1  # chasing cattle state
    st_thirst = 2  # thirsty state
    st_drink = 3  # drinking state
    st_dead = 4  # dead state

    # deletes objects if dead
    def death(self):
        canv.delete(self.id)
        return True

    # defines if cattle is next to the current predator
    def notice_cattle(self):
        if self.nearest_cattle == None:
            return False
        elif self.nearest_cattle is not self.nearest_cattle.st_drink:
            r = math.sqrt((self.nearest_cattle.coord_x - self.coord_x) ** 2 +
                          (self.nearest_cattle.coord_y - self.coord_y) ** 2)
            if r <= self.notice_radius:
                return True
            else:
                return False
        else:
            return False

    # function that controls state of thirst
    def is_thirsty(self):
        if (self.thirst > 50000 and self.state != 3) or (self.thirst > -50000 and self.state == 3):
            self.health -= 1
            return True
        else:
            return False

    # function that identifies if there is lake near cattle
    def lake_nearby(self):
        if ((self.coord_x - x_lake) / (a_axle + R)) ** 2 + ((self.coord_y - y_lake) / (b_axle + R)) ** 2 <= 1:
            return True
        else:
            return False

    # controls and changes states
    def state_machine(self):
        if (self.health < 0) or (self.hunger > 80000):
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
        self.notice_radius = 300  # radius where predator notices objects
        self.state = Predator.st_idle  # basic state is wandering around
        self.kills = 0
        self.nearest_cattle = None
        self.nearest_predator = None
        self.health = 40000
        self.velocity = 50  # predator basic speed
        self.id = canv.create_oval(self.coord_x - self.radius,
                                   self.coord_y - self.radius,
                                   self.coord_x + self.radius,
                                   self.coord_y + self.radius,
                                   fill=self.color)
        self.clock = Clock()

    # controls moving and conditions of predators
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
                self.clock.start(1)
                self.hunger += 10000
                self.thirst += 2000

            if self.state == Predator.st_chase:
                d_x = (- self.coord_x + self.nearest_cattle.coord_x)
                d_y = (- self.coord_y + self.nearest_cattle.coord_y)
                r = math.sqrt(d_x ** 2 + d_y ** 2)
                if r < self.radius:
                    self.nearest_cattle.health -= 500
                    self.hunger -= 1500
                    self.thirst += 200
                if r > 0:
                    self.velocity_x = self.velocity * d_x / r
                    self.velocity_y = self.velocity * d_y / r
                    self.hunger += 2
                    self.thirst += 2
            if self.state == Predator.st_thirst:
                d_x = (- self.coord_x + x_lake)
                d_y = (- self.coord_y + y_lake)
                r = math.sqrt(d_x ** 2 + d_y ** 2)
                self.velocity_x = self.velocity * d_x / r
                self.velocity_y = self.velocity * d_y / r
                self.hunger += 3

            if self.state == Predator.st_drink:
                self.velocity_x = 0
                self.velocity_y = 0
                self.clock.start(2)
                self.thirst -= 80
                self.health = 40000
