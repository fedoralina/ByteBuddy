import os

from tkinter import *
from qdollar.Gesture import Gesture
from qdollar.Point import Point
from qdollar.Recognizer import Recognizer

points = []
templates = []
create_template_mode = True
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
   direction = res[0].name[0]
   if direction == 'u':
      print("MOVE UP")
   elif direction == 'd':
      print("MOVE DOWN")
   elif direction == 'l':
      print("MOVE LEFT")
   elif direction == 'r':
      print("MOVE RIGHT")     
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

   

###
# tkinter GUI
###
   
canvas_width = 300
canvas_height = 200
strokeId = 0


root = Tk()
root.title( "Direction Recognizer" )
canvas = Canvas(root, 
           width=canvas_width, 
           height=canvas_height)
canvas.pack(expand = YES, fill = BOTH)
canvas.bind("<B1-Motion>", draw )
canvas.bind("<Button-3>", right_click)
canvas.bind('<ButtonRelease-1>', increase_strokeId)

label = Label( root, text = "Right Click to identify gesture", font=("Modern", 14) )
label.pack( side = BOTTOM )

if create_template_mode:
   btn_add = Button(root, text = "Add template", command=addtemplates, font=("Modern", 12))
   btn_add.pack(side = BOTTOM)

   input_template = Entry(root)
   input_template.pack()
    
mainloop()