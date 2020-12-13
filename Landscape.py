from random import *
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
length = 800
height = 500
root.geometry(str(length) + 'x' + str(height))
canv = tk.Canvas(root, bg='lime green')
canv.pack(fill=tk.BOTH, expand=1)


def lake():
    """
    :return: x_lake - lake x coord, y_lake - lake y coord, a - big axle, b - small axle
    """
    a = randint(20, 120)  # big axle
    b = randint(20, 120)  # small axle
    x_lake = randint(0, length)  # lake x coord
    y_lake = randint(0, height)  # lake y coord
    canv.create_oval(
        x_lake - a, y_lake - b, x_lake + a, y_lake + b, outline="gold",
        fill="deep sky blue", width=4
    )
    return x_lake, y_lake, a, b


(x_lake, y_lake, a_axle, b_axle) = lake()

