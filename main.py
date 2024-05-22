from camera import Camera
from cube import Cube
import numpy as np
import random


from tkinter import Tk, Canvas, Frame, BOTH

WIDTH = 800
HEIGHT = 800

class Scene:
    def __init__(self, objects: list, camera: Camera):
      self.objects = objects
      self.camera = camera

      self.random = random.choice([1, 2, 3])

    def render(self, canvas):
      for o in self.objects:
        o.render(camera, canvas)
      # pixel_color_hex = "#%02x%02x%02x" % (int(min(0.5*255, 255)), int(min(0.5*255, 255)), int(min(0.5*255, 255)))
      # canvas.create_rectangle(0, 0, 10, 10, outline="", fill=pixel_color_hex)
      # for o in self.objects:
      #   vertices = o.render(camera, canvas)
      #   for v in vertices:
      #     w = v[3]
      #     i = v[0]/w
      #     j = v[1]/w
      #     # apply pixel_color to canvas at position (i, j)
      #     pixel_color_hex = "#%02x%02x%02x" % (int(min(0.5*255, 255)), int(min(0.5*255, 255)), int(min(0.5*255, 255)))
      #     canvas.create_rectangle(i-2, j-2, i+2, j+2, outline="", fill=pixel_color_hex)
          

    def update(self, canvas):
      # Clear the canvas
      canvas.delete("all")

      # Update the position of the cube
      for o in self.objects:
        # Generate a random number between the smallest and largest of your numbers
        random_num = self.random
        random_negative = random.choice([1, 1, 1, 1, -1])
        if random_num == 1:
          o.rotate_x_axis(random_negative*np.pi/256) 
          self.random = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3])
        elif random_num == 2:
          o.rotate_y_axis(random_negative*np.pi/256) 
          self.random = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 3])
        else:
          o.rotate_z_axis(random_negative*np.pi/256) 
          self.random = random.choice([3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1])
      

      self.render(canvas)

      root.after(10, self.update, canvas)  # Update every 100 ms

            
if __name__ == "__main__":
  camera = Camera(WIDTH, HEIGHT, 200, 200, -100, -400, np.array([0, 0, -100, 1]), np.array([0, 0, -1, 0]))

  scene_objects = []
  scene_objects.append(Cube(25, np.array([0, 0, -200, 1])))

  scene_objects.append(Cube(25, np.array([100, 0, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100, 0, -200, 1])))
  scene_objects.append(Cube(25, np.array([0, 100, -200, 1])))
  scene_objects.append(Cube(25, np.array([0, -100, -200, 1])))

  scene_objects.append(Cube(25, np.array([100/2, 0, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100/2, 0, -200, 1])))
  scene_objects.append(Cube(25, np.array([0, 100/2, -200, 1])))
  scene_objects.append(Cube(25, np.array([0, -100/2, -200, 1])))

  scene_objects.append(Cube(25, np.array([100/2, 100/2, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100/2, 100/2, -200, 1])))
  scene_objects.append(Cube(25, np.array([100, 100/2, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100, 100/2, -200, 1])))

  scene_objects.append(Cube(25, np.array([100/2, -100/2, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100/2, -100/2, -200, 1])))
  scene_objects.append(Cube(25, np.array([100, -100/2, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100, -100/2, -200, 1])))


  scene_objects.append(Cube(25, np.array([100/2, 100, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100/2, 100, -200, 1])))
  scene_objects.append(Cube(25, np.array([100, 100, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100, 100, -200, 1])))

  scene_objects.append(Cube(25, np.array([100/2, -100, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100/2, -100, -200, 1])))
  scene_objects.append(Cube(25, np.array([100, -100, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100, -100, -200, 1])))



  scene = Scene(scene_objects, camera)

  root = Tk()

  canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='#1a1f1c')
  canvas.pack(fill=BOTH, expand=1)

  scene.update(canvas)

  root.mainloop()

