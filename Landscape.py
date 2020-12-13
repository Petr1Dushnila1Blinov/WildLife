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
global GO_MAIN
GO_MAIN = False



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
    btn = tk.Button(window, text="Начть симмуляцию", command = game_started)
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


def lake(canv):
    """
    :return: x_lake - lake x coord, y_lake - lake y coord, a - big axle, b - small axle
    """
    a = randint(20, 120)  # big axle
    b = randint(20, 120)  # small axle
    x_lake = randint(0, 800)  # lake x coord
    y_lake = randint(0, 500)  # lake y coord
    canv.create_oval(
        x_lake - a, y_lake - b, x_lake + a, y_lake + b, outline="gold",
        fill="deep sky blue", width=4
    )
    return x_lake, y_lake, a, b

(x_lake, y_lake, a_axle, b_axle) = lake(canv)