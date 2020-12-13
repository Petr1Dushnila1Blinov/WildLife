from Animals import *
from Neutral_Objects import *
from Landscape import *
import time


quant_cattle = 120
cattle = [0] * quant_cattle
for i in range(quant_cattle):  # Заполняем карту жертвами
    cattle[i] = Cattle()
    lcoord_x = randint(20, length - 20)
    lcoord_y = randint(20, height - 20)
    if ((x_lake - lcoord_x)/(a_axle+R))**2+((y_lake-lcoord_y)/(b_axle+R))**2 > 1:
        cattle[i].coord_x = lcoord_x
        cattle[i].coord_y = lcoord_y
    else:
        quant_cattle += 1

quant_predators = 12
predators = [0] * quant_predators
for i in range(quant_predators):  # Заполняем карту хищниками
    predators[i] = Predator()
    lcoord_x = randint(20, length - 20)
    lcoord_y = randint(20, height - 20)
    if ((x_lake - lcoord_x) / (a_axle + R)) ** 2 + ((y_lake - lcoord_y) / (b_axle + R)) ** 2 > 1:
        predators[i].coord_x = lcoord_x
        predators[i].coord_y = lcoord_y
    else:
        quant_predators += 1


RUNNING_MATYEGO = True
current_time = time.time()


def main_game():
    global delta_t, current_time, cattle, predators
    delta_t = time.time() - current_time
    current_time = time.time()

    for p in predators:  # План действия хищников
        r_min = 1000000000
        p.nearest_cattle = None
        for c in cattle:
            r = ((p.coord_x - c.coord_x) ** 2 + (p.coord_y - c.coord_y) ** 2)**0.5
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

    for c in cattle:  #Жизнь рогатого скота
        c.update()
        c.move(delta_t)


while RUNNING_MATYEGO:
    main_game()
    canv.update()

tk.mainloop()
