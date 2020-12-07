import tkinter as tk

root = tk.Tk()
fr = tk.Frame(root)
length = 800
height = 600
root.geometry(str(length) + 'x' + str(height))
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


from Animals.py import *
from Neutral_Objects.py import *
from Landscape.py import *
