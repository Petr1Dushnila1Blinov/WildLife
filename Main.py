from Animals import *
from Neutral_Objects import *
from Landscape import *
import time

quant_cattle = 1
cattle = [0] * quant_cattle
for i in range(quant_cattle):  # Заполняем карту жертвами
    cattle[i] = Cattle()
    cattle[i].coord_x = randint(20, length - 20)
    cattle[i].coord_y = randint(20, height - 20)

quant_predators = 0
predators = [0] * quant_predators
for i in range(quant_predators):  # Заполняем карту хищниками
    predators[i] = Predator()
    predators[i].coord_x = randint(20, length - 20)
    predators[i].coord_y = randint(20, height - 20)

RUNNING_MATYEGO = True
current_time = time.time()


def main_game():
    global delta_t, current_time, cattle, predators
    delta_t = time.time() - current_time
    current_time = time.time()
    for p in predators:
        r_min = 1000000000
        p.nearest_cattle = None

        for c in cattle:  # План действий хищников
            r = ((p.coord_x - c.coord_x) ** 2 + (p.coord_y - c.coord_y) ** 2) ** 0.5
            if r <= r_min:
                p.nearest_cattle = c
                r_min = r
        if p.nearest_cattle != None:
            if p.nearest_cattle.death():
                cattle.remove(p.nearest_cattle)
                del p.nearest_cattle
                p.nearest_cattle = None
        p.update()
        p.move(delta_t)

    for c in cattle:  # План действий жертв
        c.update()
        c.move(delta_t)


while RUNNING_MATYEGO:
    main_game()
    canv.update()

tk.mainloop()
