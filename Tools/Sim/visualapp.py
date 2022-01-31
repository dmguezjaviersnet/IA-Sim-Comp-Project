from tkinter import *


def nuevo():
  mensaje.set('Nuevo Fichero')

def abrir(): 
  mensaje.set('Abrir fichero')

def guardar():
  mensaje.set('Guardar fichero')

def guardar_como():
  print("Guardar fichero como")



root = Tk()
root.title('editor')

menubar = Menu (root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Nuevo", command=nuevo)
filemenu.add_command(label="Abrir", command=abrir)
filemenu.add_command(label="Guardar", command=guardar)
filemenu.add_command(label="Guardar como", command=guardar_como)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(label="Archivo", menu=filemenu)

texto = Text(root, width= 20, height=10)
texto.pack(fill='y', expand=1, side='left')
texto.config(padx=6, pady=4, bd=0, font=("Consolas", 12))



# Monitor inferior
mensaje = StringVar()
mensaje.set('Bienvenido a tu editor')
monitor = Label(root, textvar=mensaje, justify='right')
monitor.pack(side='bottom')


def checkered(canvas, line_distance):
  # vertical lines at an interval of "line_distance" pixel
  for x in range(line_distance,canvas_width,line_distance):
    canvas.create_line(x, 0, x, canvas_height, fill="#476042")
  # horizontal lines at an interval of "line_distance" pixel
  for y in range(line_distance,canvas_height,line_distance):
    canvas.create_line(0, y, canvas_width, y, fill="#476042")


canvas_width = 200
canvas_height = 100


w = Canvas(root, width=canvas_width, height=canvas_height)
w.pack(side='left')

checkered(w,10)

root.config(menu= menubar)
root.mainloop()
