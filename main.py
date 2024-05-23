from camera import Camera
from cube import Cube
import numpy as np
import random
import keyboard


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
          

    def update(self, canvas):
      # Get currently pressed keys
      
      keyboard.start_recording()
      currently_pressed = keyboard._pressed_events
      
      for event in currently_pressed:
        if event == 75: # key l_arrow
          camera.rotate_y_axis(-np.pi/128)
        if event == 77: # key r_arrow
          camera.rotate_y_axis(np.pi/128)
        if event == 72: # key up_arrow
          camera.rotate_bas_u_axis(np.pi/128)
        if event == 80: # key down_arrow
          camera.rotate_bas_u_axis(-np.pi/128)

        if event == 16: # key Q
          camera.translate(5*camera.v)    
        if event == 18: # key E
          camera.translate(-5*camera.v)  
        if event == 17: # key W
          camera.translate(-5*camera.w)
        if event == 30: # key A
          camera.translate(5*camera.u)
        if event == 31: # key S
          camera.translate(5*camera.w)
        if event == 32: # key D
          camera.translate(-5*camera.u)
      
      # Clear the canvas
      canvas.delete("all")

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

      root.after(10, self.update, canvas)  # Update every 10 ms

      keyboard.stop_recording()

            
if __name__ == "__main__":
  camera = Camera(WIDTH, HEIGHT, 200, 200, -200, -4000, np.array([0, 0, -10, 1]), np.array([0, 0, -1, 0]))

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

  

