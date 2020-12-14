from Animals import *
from Landscape import *
import time


def create_started_window():
    window = tk.Tk()
    window.title("WildLife simulator")
    window.geometry('800x500')
    lbl = tk.Label(window, text="Наша команда приветствет Вас в WildLife simulator", font=("Arial Bold", 14))
    lbl.grid(column=0, row=0)
    global GO_MAIN

    def game_started():
        global GO_MAIN
        if GO_MAIN:
            btn['fg'] = "black"
            btn['text'] = "Продолжить показ симмуляции"
            GO_MAIN = False
        else:
            btn['fg'] = "red"
            btn['text'] = "Приостановить показ симмуляции"
            GO_MAIN = True
    btn = tk.Button(window, text="Начать симмуляцию", command = game_started)
    btn.grid(column=0, row=2)
    k_predator = tk.DoubleVar()
    lbl_predator = tk.Label(window, text="Кол-во Хищников", font=("Arial Bold", 14))
    lbl_predator.grid(column=0, row=3)
    scale_predator = tk.Scale(window, variable=k_predator, orient=tk.HORIZONTAL)
    scale_predator.grid(column=0, row=4)
    k_animal = tk.DoubleVar()
    lbl_animal = tk.Label(window, text="Кол-во Травоядных", font=("Arial Bold", 14))
    lbl_animal.grid(column=2, row=3)
    scale_animal = tk.Scale(window, variable=k_animal, orient=tk.HORIZONTAL)
    scale_animal.grid(column=2, row=4)

global length, heigth
length, height = 800, 600

quant_cattle = 230
cattle = [0] * quant_cattle
for i in range(quant_cattle):  # Заполняем карту жертвами
    cattle[i] = Cattle()
    cattle[i].coord_x = randint(20, length - 20)
    cattle[i].coord_y = randint(20, height - 20)

quant_predators = 12
predators = [0] * quant_predators
for i in range(quant_predators):  # Заполняем карту хищниками
    predators[i] = Predator()
    predators[i].coord_x = randint(20, length - 20)
    predators[i].coord_y = randint(20, length - 20)


RUNNING_MATYEGO = True
GO_START = True
current_time = time.time()


def main_game():
    global delta_t, current_time, cattle, predators
    delta_t = time.time() - current_time
    current_time = time.time()

    for p in predators:  # План действия хищников
        r_min = 1000000000
        p.nearest_cattle = None
        for c in cattle:
            r = ((p.coord_x - c.coord_x) ** 2 + (p.coord_y - c.coord_y) ** 2) ** 0.5
            if r <= r_min:
                p.nearest_cattle = c
                r_min = r
        if p.nearest_cattle is not None:
            if p.nearest_cattle.death():
                cattle.remove(p.nearest_cattle)
                del p.nearest_cattle
                p.nearest_cattle = None
        p.update()
        p.move(delta_t)

    for c in cattle:  # Жизнь рогатого скота
        while ((c.coord_x - x_lake) / (a_axle + 0.6 * R)) ** 2 + ((c.coord_y - y_lake) / (b_axle + 0.6 * R)) ** 2 <= 1:
            c.coord_x = randint(20, length - 20)
            c.coord_y = randint(20, length - 20)
        c.update()
        c.move(delta_t)



while RUNNING_MATYEGO:
    if GO_MAIN:
        main_game()
    else:
        if GO_START:
            create_started_window()
            GO_START = False
    canv.update()

tk.mainloop()
