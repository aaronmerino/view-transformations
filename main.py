from camera import Camera
from cube import Cube
import numpy as np
import math

from tkinter import Tk, Canvas, Frame, BOTH

WIDTH = 400
HEIGHT = 400

class Scene:
    def __init__(self, objects: list, camera: Camera):
       self.objects = objects
       self.camera = camera

    def render(self, canvas):
      for o in self.objects:
        vertices = o.render(camera)
        for v in vertices:
          w = v[3]
          i = v[0]/w
          j = v[1]/w
          # apply pixel_color to canvas at position (i, j)
          pixel_color_hex = "#%02x%02x%02x" % (int(min(0.5*255, 255)), int(min(0.5*255, 255)), int(min(0.5*255, 255)))
          canvas.create_rectangle(i-2, j-2, i+2, j+2, outline="", fill=pixel_color_hex)

    def update(self, canvas):
        # Clear the canvas
        canvas.delete("all")

        # Update the position of the cube
        for o in self.objects:
            o.rotate_y_axis(np.pi/32)  

        self.render(canvas)

        root.after(40, self.update, canvas)  # Update every 100 ms

            
if __name__ == "__main__":
  camera = Camera(WIDTH, HEIGHT, 100, 100, -100, -400, np.array([0, 0, 0, 1]), np.array([0, 0, -1, 0]))

  scene_objects = []
  scene_objects.append(Cube(50, np.array([0, 0, -120, 1])))

  scene = Scene(scene_objects, camera)

  root = Tk()

  canvas = Canvas(root, width=WIDTH, height=HEIGHT)
  canvas.pack(fill=BOTH, expand=1)

  scene.update(canvas)

  root.mainloop()

