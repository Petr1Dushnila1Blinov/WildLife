from random import *
import tkinter as tk
import math
import time

root = tk.Tk()
fr = tk.Frame(root)
length = 800
height = 600
root.geometry(str(length) + 'x' + str(height))
canv = tk.Canvas(root, bg='lime green')
canv.pack(fill=tk.BOTH, expand=1)

def lake():
    global M
    M = 10**3
    a = randint(20, 120)
    b = randint(20, 120)
    x = randint(0, length)
    y = randint(0, height)
    canv.create_oval(
        x-a, y-b, x+a, y+b, outline="gold",
        fill="deep sky blue", width=4
    )
    return (x, y, a, b)

(x_lake, y_lake, a_axle, b_axle) = lake()

tk.mainloop()