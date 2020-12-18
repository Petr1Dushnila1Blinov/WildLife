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


def food_generation():
    global fruits
    old_count = len(fruits)
    quant_fruits = 1 * int(scale_fruit.get())
    new_fruits = [0] * (quant_fruits)
    fruits += new_fruits
    for i in range(old_count, len(fruits)):  # filling map with fruits
        fruits[i] = Fruit()
        fruits[i].coord_x = randint(20, length - 20)
        fruits[i].coord_y = randint(20, height - 20)



food_time = time.time()
start_time = time.time()
# head function
def main_game():
    global delta_t, current_time, cattle, predators, grass, DETERMINED, quant_cattle, quant_predators, quant_fruits, food_time, start_time
    # if still works
    if not DETERMINED:
        determine_quantities_animals()
        determine_fruits()
        DETERMINED = True

    # period of update
    delta_t = time.time() - current_time
    current_time = time.time()
    food_time += delta_t
    for p in predators:  # predators action
        if p.state == 0:
            while ((p.coord_x - x_lake) / (a_axle + 0.5 * R)) ** 2 + (
                    (p.coord_y - y_lake) / (b_axle + 0.5 * R)) ** 2 <= 1:
                p.coord_x = randint(20, length - 20)
                p.coord_y = randint(20, height - 20)
        if p.state == 4:
            predators.remove(p)
            quant_predators -= 1
        r_min = 1000000000
        r_taken_min = 1000000000
        if p.state != 2 and p.state != 3:
            if (not p.nearest_cattle == None) and \
                    ((p.coord_x - p.nearest_cattle.coord_x) ** 2 + (p.coord_y - p.nearest_cattle.coord_y) ** 2) ** 0.5 < \
                    0.1*p.notice_radius:
                pass
            else:
                if not p.nearest_cattle == None:
                    p.nearest_cattle.under_attack = False
                    p.nearest_cattle.color = 'green'
                    canv.itemconfig(p.nearest_cattle.id,
                                    fill=p.nearest_cattle.color)
                nearest_target = None
                p.nearest_cattle = None
                nearest_taken_cattle = None
                p.nearest_predator = None
                for c in cattle:
                    r = ((p.coord_x - c.coord_x) ** 2 + (p.coord_y - c.coord_y) ** 2) ** 0.5  # distance from cattle to predator
                    if r < 0.08 * p.notice_radius and r < r_min:
                        nearest_target = c
                        r_min = r
                    else:
                        if r < p.notice_radius and r<r_min and not c.under_attack:
                            nearest_target = c

                            r_min = r
                        else:
                            if r<p.notice_radius and r<r_taken_min:
                                nearest_taken_cattle = c
                                r_taken_min = r
                if nearest_target == None and not nearest_taken_cattle == None:
                    nearest_target = nearest_taken_cattle

                if p.nearest_cattle != nearest_target and p.nearest_cattle != None :
                    p.nearest_cattle.under_attack = False
                    p.nearest_cattle.color = 'green'
                    canv.itemconfig(p.nearest_cattle.id,
                                    fill=p.nearest_cattle.color)
                p.nearest_cattle = nearest_target
            if not p.nearest_cattle == None:
                if p.nearest_cattle.death():
                    if p.nearest_cattle in cattle:
                        cattle.remove(p.nearest_cattle)
                    quant_cattle -= 1
                    del p.nearest_cattle
                    p.nearest_cattle = None
                else:
                    p.nearest_cattle.under_attack = True
                    p.nearest_cattle.color = 'green3'
                    canv.itemconfig(p.nearest_cattle.id,
                                    fill=p.nearest_cattle.color)
        elif p.nearest_cattle is not None:
            p.nearest_cattle.under_attack = False
            p.nearest_cattle.color = 'green'
            canv.itemconfig(p.nearest_cattle.id,
                            fill=p.nearest_cattle.color)

        """for c in cattle:
            r = ((p.coord_x - c.coord_x) ** 2 + (p.coord_y - c.coord_y) ** 2) ** 0.5  # distance from cattle to predator
            if r <= r_min:
                p.nearest_target = c  # defines nearest cattle
                r_min = r
        if p.nearest_target is not None:  # if it could define a particular cattle next to predator
            if p.nearest_target.death():
                cattle.remove(p.nearest_target)
                quant_cattle -= 1
                del p.nearest_target
                p.nearest_target = None"""
        for k in predators:
            if p == k:
                pass
            else:
                r = ((p.coord_x - k.coord_x) ** 2 + (p.coord_y - k.coord_y) ** 2) ** 0.5  # distance from predator
                if r <= r_min:  # to predator
                    p.nearest_predator = k  # defines nearest cattle
                    r_min = r
        # print('Здоровье: ', p.health, 'Жажда: ', p.thirst, 'Голод: ', p.hunger)
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



    for f in fruits:  # fruits life
        while ((f.coord_x - x_lake) / (2*a_axle)) ** 2 + (
                (f.coord_y - y_lake) / (2*b_axle)) ** 2 <= 1:
            f.coord_x = randint(20, length - 20)
            f.coord_y = randint(20, height - 20)
        if f.state == 3:
            fruits.remove(f)
            quant_fruits -= 1
        f.update()
    if food_time - start_time > 4:
        food_generation()
        food_time = time.time()
        start_time = time.time()
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
