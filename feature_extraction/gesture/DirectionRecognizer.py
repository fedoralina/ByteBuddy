import os

from tkinter import *
import tkinter.font as font
from qdollar.Gesture import Gesture
from qdollar.Point import Point
from qdollar.Recognizer import Recognizer

points = []
templates = []
create_template_mode = False
template_name = "NAME"

def draw(event):
   color = "#000000"
   points.append(Point(int(event.x), int(event.y), int(strokeId)))
   x1, y1 = ( event.x - 1 ), ( event.y - 1 )
   x2, y2 = ( event.x + 1 ), ( event.y + 1 )
   canvas.create_oval( x1, y1, x2, y2, fill = color )

def right_click(event):
   global points
   canvas.delete('all')
   gesture = Gesture("", points)
   res = Recognizer().classify(gesture, templates)
   template_name = res[0].name.split('.')[0]
   if template_name == 'u':
      print("MOVE UP")
   elif template_name == 'd':
      print("MOVE DOWN")
   elif template_name == 'l':
      print("MOVE LEFT")
   elif template_name == 'r':
      print("MOVE RIGHT")   
   else:
      print(f"Q$ recognized: {template_name}")  
   points = []

def increase_strokeId(event):
   global strokeId
   strokeId+=1

def addtemplates():
   template = Gesture(input_template.get(), points)
   templates.append(template)
   canvas.delete('all')
   input_template.delete(0, END)

   if create_template_mode:
      print("CREATE TEMPLATE CALLED")
      with open('templates/' + template.name + '.txt', 'w') as f:
         for i in range(len(template.Points)):
            point = template.Points[i]
            f.write(f"{int(point.intX)} {int(point.intY)} {point.strokeId}\n")
      
 
# read templates
for filename in os.listdir("templates/"):
   path = os.path.join('templates/',filename)
   f1 = open(path,'r')
   f1 = f1.readlines()
   points = []
   for line in f1:
      x,y,strokeId = line.split(" ")
      points.append(Point(int(x),int(y),int(strokeId)))
   template = Gesture(filename, points)
   templates.append(template)

points = []

###
# tkinter GUI
###
   
canvas_width = 200
canvas_height = 100
strokeId = 0

root = Tk()
root.title( "Direction Recognizer" )
root.geometry("800x500")
root.resizable(width=False, height=False)

bg_color = "#a8d7e9"
font_style = font.Font(family="Helvetica", size= 12)

root.configure(bg=bg_color)


label = Label(root, text = "Tap with 2 fingers to move", font=font_style, bg="lightgrey")
label.pack(side=BOTTOM )

canvas = Canvas(root, 
           width=canvas_width, 
           height=canvas_height,
           bg="#546c75")
canvas.pack(expand = NO, side=BOTTOM)
canvas.bind("<B1-Motion>", draw )
canvas.bind("<Button-3>", right_click)
canvas.bind('<ButtonRelease-1>', increase_strokeId)



if create_template_mode:
   btn_add = Button(root, text = "Add template", command=addtemplates, font=font_style)
   btn_add.pack(side = BOTTOM)

   input_template = Entry(root, font= font_style)
   input_template.pack(side=BOTTOM)
    
root.mainloop()