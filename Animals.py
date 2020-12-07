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


