from Animals import *
from Neutral_Objects import *
from Landscape import *

quant_cattle = 4
cattle = [0] * quant_cattle
for i in range(quant_cattle):
    cattle[i] = Cattle()

quant_predators = 2
predators = [0] * quant_predators
for i in range(quant_predators):
    predators[i] = Predator()

RUNNING_MATYEGO = True

def main_game():
    for p in predators:
        r_min = 1000000000
        p.nearest_cattle = None
        for c in cattle:
            r = math.sqrt((p.coord_x - c.coord_x) ** 2 + (p.coord_y - c.coord_y) ** 2)
            if r <= r_min:
                p.nearest_cattle = c
                r_min = r
        p.update()
        p.move()
    for c in cattle:
        c.move()


while RUNNING_MATYEGO:
    main_game()
tk.mainloop()