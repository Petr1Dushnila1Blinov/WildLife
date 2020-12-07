from Animals import *
from Neutral_Objects import *
from Landscape import *
import time
quant_cattle = 4
cattle = [0] * quant_cattle
for i in range(quant_cattle):
    cattle[i] = Cattle()
    cattle[i].coord_x = length - 200
    cattle[i].coord_y = height - 200

quant_predators = 2
predators = [0] * quant_predators
for i in range(quant_predators):
    predators[i] = Predator()
    predators[i].coord_x = 500 + i * 20
    predators[i].coord_y = 350

RUNNING_MATYEGO = True
current_time = time.time()


def main_game():
    global delta_t, current_time
    delta_t = time.time() - current_time
    current_time = time.time()
    for p in predators:

        r_min = 1000000000
        p.nearest_cattle = None
        for c in cattle:
            r = math.sqrt((p.coord_x - c.coord_x) ** 2 + (p.coord_y - c.coord_y) ** 2)
            if r <= r_min:
                p.nearest_cattle = c
                r_min = r
        p.update()
        p.move(delta_t)
    for c in cattle:
        if c.death():
            cattle.remove(c)
        c.update()
        c.move(delta_t)


while RUNNING_MATYEGO:
    main_game()
    canv.update()


tk.mainloop()