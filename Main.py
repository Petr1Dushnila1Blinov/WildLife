from Animals import *
from Neutral_Objects import *
from Landscape import *

cattle_1 = Cattle()
predator_1 = Predator()

cattle = [cattle_1]
predators = [predator_1]

def main_game():
    for p in predators:
        for c in cattle:
            break
        p.move()
    for c in cattle:
        c.move()