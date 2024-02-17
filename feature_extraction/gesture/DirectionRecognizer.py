import os

from tkinter import *
import tkinter.font as font
from gesture.qdollar.Gesture import Gesture
from gesture.qdollar.Point import Point
from gesture.qdollar.Recognizer import Recognizer


class DirectionRecognizer():

   def __init__(self):
      self.points = []
      self.templates = []
      self.create_template_mode = False
      self.template_name = "NAME"   
      self.strokeId = 0
      self.input_template = None
      self.canvas = None

   def draw(self, event):
      color = "#000000"
      self.points.append(Point(int(event.x), int(event.y), int(self.strokeId)))
      x1, y1 = ( event.x - 1 ), ( event.y - 1 )
      x2, y2 = ( event.x + 1 ), ( event.y + 1 )
      self.canvas.create_oval( x1, y1, x2, y2, fill = color )

   def right_click(self, event):
      self.canvas.delete('all')
      gesture = Gesture("", self.points)
      res = Recognizer().classify(gesture, self.templates)
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
      self.points = []

   def increase_strokeId(self, event):
      self.strokeId+=1

   def addtemplates(self):
      template = Gesture(self.input_template.get(), self.points)
      self.templates.append(template)
      self.canvas.delete('all')
      self.input_template.delete(0, END)

      if self.create_template_mode:
         print("CREATE TEMPLATE CALLED")
         with open('gesture/templates/' + template.name + '.txt', 'w') as f:
            for i in range(len(template.Points)):
               point = template.Points[i]
               f.write(f"{int(point.intX)} {int(point.intY)} {point.strokeId}\n")
      
   def read_templates(self):
      for filename in os.listdir("gesture/templates/"):
         path = os.path.join('gesture/templates/',filename)
         f1 = open(path,'r')
         f1 = f1.readlines()
         points = []
         for line in f1:
            x,y,strokeId = line.split(" ")
            points.append(Point(int(x),int(y),int(strokeId)))
         template = Gesture(filename, points)
         self.templates.append(template)

      self.points = []

   ###
   # tkinter GUI
   ###
   def draw_GUI(self):

      canvas_width = 200
      canvas_height = 100

      root = Tk()
      root.title( "Direction Recognizer" )
      root.geometry("800x500")
      root.resizable(width=False, height=False)

      bg_color = "#a8d7e9"
      font_style = font.Font(family="Helvetica", size= 12)
      root.configure(bg=bg_color)

      label = Label(root, text = "Tap with 2 fingers to move", font=font_style, bg="lightgrey")
      label.pack(side=BOTTOM )

      self.canvas = Canvas(root, 
               width=canvas_width, 
               height=canvas_height,
               bg="#546c75")
      self.canvas.pack(expand = NO, side=BOTTOM)
      self.canvas.bind("<B1-Motion>", self.draw )
      self.canvas.bind("<Button-3>", self.right_click)
      self.canvas.bind('<ButtonRelease-1>', self.increase_strokeId)

      if self.create_template_mode:
         btn_add = Button(root, text = "Add template", command=self.addtemplates, font=font_style)
         btn_add.pack(side = BOTTOM)

         self.input_template = Entry(root, font= font_style)
         self.input_template.pack(side=BOTTOM)
         
      root.mainloop()