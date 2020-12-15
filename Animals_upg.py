import math
global R
R = 10
# from contracts import contract

from Landscape import *


def lake_force(mass, x_coord, y_coord):
    """
            :param mass: float, >0, масса зверя
            :param x_coord: float, собственная координата x
            :param y_coord: float, собственная координата y
    """
    r = math.sqrt((x_coord - x_lake) ** 2 + (y_coord - y_lake) ** 2)
    force_x = mass * M / r ** 2 * (x_coord - x_lake) / r
    force_y = mass * M / r ** 2 * (y_coord - y_lake) / r
    return force_x, force_y


def obj_force(obj, mass, x_coord, y_coord, x_obj, y_obj, MASS):
    """
            :param obj: объект
            :param mass: float, >0, масса
            :param x_coord: float, собственная координата x
            :param y_coord: float, собственная координата y
            :param x_obj: float, координата x объекта
            :param y_obj: float, координата y объекта
            :param MASS: float, >0, масса объекта
    """
    r = math.sqrt((x_coord - x_obj) ** 2 + (y_coord - y_obj) ** 2)
    force_x = mass * MASS / r ** 2 * (x_coord - x_obj) / r
    force_y = mass * MASS / r ** 2 * (y_coord - y_obj) / r
    return force_x, force_y


# Timer
class Clock:
    def __init__(self):
        self.is_running = False
        self.stop_time = 0

    # makes time flowing
    def start(self, period):
        """
        :param period: update time
        """
        self.is_running = True
        self.stop_time = time.time() + period

    # stops time flowing
    def update(self):
        if time.time() > self.stop_time:
            self.is_running = False


class Animal:
    def __init__(self):
        self.coord_x = 1  # x coordinate
        self.coord_y = 1  # y coordinate
        self.velocity = 0  # common speed
        self.anspeed = 0 #  angle velocity
        self.anaccel = 0 # angle acceleration
        self.angle = 0  # motion direction
        self.hunger = 0  # represents how hungry the animal is
        self.thirst = 0  # represents how thirsty the animal is
        self.health = 100  # represents the health points
        self.mass = 10 ** 3  # mass of the animal
        self.radius = R # radius of image
        self.color = 'green'
        # creates the image of an animal

    def move(self, delta_t):
        """
        :param delta_t: update time
        """
        self.coord_x += self.velocity * math.cos(self.angle) * delta_t
        self.coord_y += self.velocity * math.sin(self.angle) * delta_t
        if self.coord_x < self.radius:
            if self.angle > math.pi:
                self.angle = math.pi * 1.5
                self.anaccel = -0.2
            else:
                self.angle = math.pi * 0.5
                self.anaccel = 0.2
            self.coord_x = self.radius
        if self.coord_x > length-self.radius:
            if self.angle <= math.pi:
                self.angle = math.pi * 0.5
                self.anaccel = -0.2
            else:
                self.angle = math.pi * 1.5
                self.anaccel = 0.2
            self.coord_x = length-self.radius
        if self.coord_y < self.radius:
            if math.pi * 0.5 < self.angle < math.pi * 1.5:
                self.angle = math.pi
                self.anaccel = -0.2
            else:
                self.angle = 0
                self.anaccel = 0.2
            self.coord_y = self.radius
        if self.coord_y > height-self.radius:
            if math.pi * 0.5 < self.angle < math.pi * 1.5:
                self.angle = math.pi
                self.anaccel = 0.2
            else:
                self.angle = 0
                self.anaccel = -0.2
            self.coord_y = height-self.radius

        if ((x_lake-self.coord_x)/(a_axle+self.radius))**2 + ((y_lake-self.coord_y)/(b_axle+self.radius))**2 <= 1:
            smangle = math.atan((self.coord_y - y_lake) / (self.coord_x - x_lake))
            gamma = math.atan(-b_axle / a_axle * 1 / math.tan(smangle))
            if gamma + math.pi/2 >= self.angle:
                self.angle = gamma
                self.anaccel = 2
            else:
                self.angle = 2*math.pi - gamma
                self.anaccel = -2
            self.coord_x = x_lake + (a_axle + self.radius)*math.cos(smangle)#+ abs(math.pi-smangle)/(math.pi-smangle)
            self.coord_y = y_lake + (b_axle + self.radius)*math.sin(smangle)#+ abs(math.pi-smangle)/(math.pi-smangle)


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
        self.velocity = 50
        self.angle = randint(0, 359)/360 * 2*math.pi
        self.anspeed = randint(-50, 50)/1000
        self.anaccel = randint(-100, 100)/100
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
        V = 50  # Скорость движения жертв
        self.clock.update()
        if not self.clock.is_running:
            if abs(self.anaccel) > 1:
                if self.anaccel > 0:
                    self.anaccel -= 0.1
                else:
                    self.anaccel += 0.1
            else:
                self.anaccel = randint(-10, 10)/200
            if abs(self.anspeed) > 0.25:
                if self.anspeed > 0:
                    self.anspeed -= 0.02
                else:
                    self.anspeed += 0.02
            else:
                self.anspeed += self.anaccel/100
            self.angle += self.anspeed
            self.angle %= (2*math.pi)
            self.clock.start(0.1)


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
        self.velocity = 50  # Скорость передвижения хищников
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


