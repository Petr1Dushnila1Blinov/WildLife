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


def main_game():
    for p in predators:
        for c in cattle:
            break
        p.move()
    for c in cattle:
        c.move()