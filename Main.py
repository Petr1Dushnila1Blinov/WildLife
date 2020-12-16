from Animals import *
from Landscape import *
from Clock import *
import time
import matplotlib.pyplot as plt


# creates control window
def create_started_window():
    # creates main menu 300X300
    window = tk.Tk()
    window.title("WildLife simulator")
    window.geometry('300x300')
    lbl = tk.Label(window, text="   Welcome to WildLife simulator", font=("Arial Bold", 14))
    lbl.grid(column=0, row=0)
    global GO_MAIN, scale_predator, scale_animal, scale_fruit

    # changes the state of inscription
    def game_started():
        global GO_MAIN
        if GO_MAIN:
            btn_start['fg'] = "black"
            btn_start['text'] = "Keep watching"
            GO_MAIN = False
        else:
            btn_start['fg'] = "red"
            btn_start['text'] = "Stop showing"
            GO_MAIN = True

    btn_start = tk.Button(window, text="Start simulation", command=game_started)
    btn_start.grid(column=0, row=2)

    # controls if game is over
    def game_ended():
        root.destroy()
        window.destroy()
        global GO_MAIN, GO_START, DESTROYED
        GO_MAIN = False
        GO_START = True
        DESTROYED = True
        print_statistics("test.png")

    # creates buttons for different aims
    btn_end = tk.Button(window, text="Finish Simulation", command=game_ended)
    btn_end.grid(column=0, row=9)
    lbl_predator = tk.Label(window, text="Predators Quantity", font=("Arial Bold", 14))
    lbl_predator.grid(column=0, row=3)
    scale_predator = tk.Scale(window, orient=tk.HORIZONTAL)
    scale_predator.grid(column=0, row=4)
    lbl_animal = tk.Label(window, text="Cattle Quantity", font=("Arial Bold", 14))
    lbl_animal.grid(column=0, row=5)
    scale_animal = tk.Scale(window, orient=tk.HORIZONTAL)
    scale_animal.grid(column=0, row=6)
    lbl_fruit = tk.Label(window, text="Fruit Scale", font=("Arial Bold", 14))
    lbl_fruit.grid(column=0, row=7)
    scale_fruit = tk.Scale(window, orient=tk.HORIZONTAL)
    scale_fruit.grid(column=0, row=8)


global length, heigth
length, height = 800, 600


# function determines animals quantity
def determine_quantities_animals():
    global quant_cattle, cattle, quant_predators, predators
    quant_cattle = 2 * int(scale_animal.get())  # takes quantity of cattle from SCALE in main menu
    cattle = [0] * quant_cattle
    for i in range(quant_cattle):  # filling map with cattle
        cattle[i] = Cattle()
        cattle[i].coord_x = randint(20, length - 20)
        cattle[i].coord_y = randint(20, height - 20)

    quant_predators = 1 * int(scale_predator.get())  # takes quantity of predators from SCALE in main menu
    predators = [0] * quant_predators
    for i in range(quant_predators):  # filling map with predators
        predators[i] = Predator()
        predators[i].coord_x = randint(20, length - 20)
        predators[i].coord_y = randint(20, height - 20)

def determine_fruits():
    global quant_fruits, fruits
    quant_fruits = 1 * int(scale_fruit.get())  # takes quantity of growing fruits from SCALE in main menu
    fruits = [0] * quant_fruits
    for i in range(quant_fruits):  # filling map with fruits
        fruits[i] = Fruit()
        fruits[i].coord_x = randint(20, length - 20)
        fruits[i].coord_y = randint(20, height - 20)



RUNNING_MATYEGO = True
GO_START = True
DESTROYED = False
DETERMINED = False
current_time = time.time()


# head function
def main_game():
    global delta_t, current_time, cattle, predators, grass, DETERMINED, quant_cattle, quant_predators, quant_grass
    # if still works
    if not DETERMINED:
        determine_quantities_animals()
        determine_fruits()
        DETERMINED = True

    # period of update
    delta_t = time.time() - current_time
    current_time = time.time()

    for p in predators:  # predators action
        if p.state == 0:
            while ((p.coord_x - x_lake) / (a_axle + 0.5 * R)) ** 2 + ((p.coord_y - y_lake) / (b_axle + 0.5 * R)) ** 2 <= 1:
                p.coord_x = randint(20, length - 20)
                p.coord_y = randint(20, height - 20)
        if p.state == 4:
            predators.remove(p)
            quant_predators -= 1
        r_min = 1000000000
        p.nearest_cattle = None
        p.nearest_predator = None
        for c in cattle:
            r = ((p.coord_x - c.coord_x) ** 2 + (p.coord_y - c.coord_y) ** 2) ** 0.5  # distance from cattle to predator
            if r <= r_min:
                p.nearest_cattle = c  # defines nearest cattle
                r_min = r
        if p.nearest_cattle is not None:  # if it could define a particular cattle next to predator
            if p.nearest_cattle.death():
                cattle.remove(p.nearest_cattle)
                quant_cattle -= 1
                del p.nearest_cattle
                p.nearest_cattle = None
        for k in predators:
            if p == k:
                pass
            else:
                r = ((p.coord_x - k.coord_x) ** 2 + (p.coord_y - k.coord_y) ** 2) ** 0.5  # distance from predator
                if r <= r_min:                                                            # to predator
                    p.nearest_predator = k  # defines nearest cattle
                    r_min = r
        #print('Здоровье: ', p.health, 'Жажда: ', p.thirst, 'Голод: ', p.hunger)
        p.update()
        p.move(delta_t)

    for c in cattle:  # cattle life
        while ((c.coord_x - x_lake) / (a_axle + 0.6 * R)) ** 2 + ((c.coord_y - y_lake) / (b_axle + 0.6 * R)) ** 2 <= 1:
            c.coord_x = randint(20, length - 20)
            c.coord_y = randint(20, height - 20)
        r_min = 1000000000
        for p in predators:
            r = ((p.coord_x - c.coord_x) ** 2 + (p.coord_y - c.coord_y) ** 2) ** 0.5  # distance from cattle to predator
            if r <= r_min:
                c.nearest_predator = p  # defines nearest predactor
                r_min = r
        c.update()
        c.move(delta_t)

    for f in fruits:   # fruits life
        if f.state == 3:
            grass.remove(f)
            quant_fruits -= 1
        f.update()

    write_statistics(delta_t)  # writes quantity and time in massives below



Time = []
time_live = 0
Quant_cattle = []
Quant_predators = []
Quant_fruits = []


# remembers statistics to print it further(uses matplotlib)
def write_statistics(delta_t):
    """
    :param delta_t: update time
    """
    global quant_cattle, quant_predators, \
        Quant_cattle, Quant_predators, Time, time_live

    plt.xlabel(r"$time,\ с$")
    plt.ylabel(r"$Quantity\  of\  animals$")
    plt.title(r"$Quantity(t)$")
    Quant_cattle.append(quant_cattle)
    Quant_predators.append(quant_predators)
    time_live += delta_t
    Time.append(time_live)


# shows graphics after simulation
def print_statistics(file: str):
    """
    :param file: filename.format
    :return: graphics of population
    """
    global Time, Quant_predators, Quant_cattle
    plt.plot(Time, Quant_cattle, 'ro', color='green', markersize=2, label='Травоядные')
    plt.plot(Time, Quant_predators, 'ro', color='red', markersize=2, label='Хищники')
    plt.legend(loc='upper right', fontsize=10)
    plt.savefig(file)
    plt.show()


# mainloop
while RUNNING_MATYEGO:
    if GO_MAIN:
        main_game()
    else:
        if GO_START:
            create_started_window()
            GO_START = False
    if not DESTROYED:
        canv.update()

tk.mainloop()