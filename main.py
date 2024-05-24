from camera import Camera
from cube import Cube
import numpy as np
import random
import keyboard
from pynput.mouse import Controller
from pynput import mouse


from tkinter import Tk, Canvas, Frame, BOTH

WIDTH = 800
HEIGHT = 800



class Scene:
  def __init__(self, objects: list, camera: Camera):
    self.objects = objects
    self.camera = camera

    self.random = random.choice([1, 2, 3])

    self.prev_mouse_x = None
    self.control_cam = True

    def on_click(x, y, button, pressed):
      if pressed:
        if root.winfo_rootx() <= x <= root.winfo_rootx() + root.winfo_width() and root.winfo_rooty() <= y <= root.winfo_rooty() + root.winfo_height():
          self.control_cam = not self.control_cam
      # if not pressed:
      #     self.control_cam = False

    listener = mouse.Listener(on_click=on_click)
    listener.start()

  def render(self, canvas):
    for o in self.objects:
      o.render(camera, canvas)
        

  def update(self, canvas):

    mouse = Controller()

    if self.prev_mouse_x is None:
      self.prev_mouse_x = mouse.position
    else:
      if not (self.prev_mouse_x == mouse.position) and self.control_cam:
        # print(np.array(mouse.position) - np.array(self.prev_mouse_x))
        mouse_difference = np.array(mouse.position) - np.array(self.prev_mouse_x)

        camera.rotate_y_axis(mouse_difference[0]*np.pi/1024)
        camera.rotate_bas_u_axis(-mouse_difference[1]*np.pi/1024)
        self.prev_mouse_x = mouse.position

        mouse.position = (root.winfo_x() + (root.winfo_width()//2), root.winfo_y() +  (root.winfo_height()//2))
        self.prev_mouse_x = (root.winfo_x() + (root.winfo_width()//2), root.winfo_y() + (root.winfo_height()//2))
          
    # Get currently pressed keys
    
    keyboard.start_recording()
    currently_pressed = dict(keyboard._pressed_events)
    
    for event in currently_pressed:
      if event == 1: # esc key
        self.control_cam = False
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

    root.after(1, self.update, canvas)  # Update every 10 ms

    keyboard.stop_recording()

            
if __name__ == "__main__":
  camera = Camera(WIDTH, HEIGHT, 200, 200, -140, -4000, np.array([0, 0, -10, 1]), np.array([0, 0, -1, 0]))

  scene_objects = []
  scene_objects.append(Cube(25, np.array([0, 0, -200, 1])))

  scene_objects.append(Cube(25, np.array([150, 0, -200, 1])))
  scene_objects.append(Cube(25, np.array([-150, 0, -200, 1])))
  scene_objects.append(Cube(25, np.array([0, 150, -200, 1])))
  scene_objects.append(Cube(25, np.array([0, -150, -200, 1])))

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
  # scene_objects.append(Cube(25, np.array([100, 100/2, -200, 1])))
  # scene_objects.append(Cube(25, np.array([-100, 100/2, -200, 1])))

  scene_objects.append(Cube(25, np.array([100/2, -100/2, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100/2, -100/2, -200, 1])))
  # scene_objects.append(Cube(25, np.array([100, -100/2, -200, 1])))
  # scene_objects.append(Cube(25, np.array([-100, -100/2, -200, 1])))


  # scene_objects.append(Cube(25, np.array([100/2, 100, -200, 1])))
  # scene_objects.append(Cube(25, np.array([-100/2, 100, -200, 1])))
  # scene_objects.append(Cube(25, np.array([100, 100, -200, 1])))
  # scene_objects.append(Cube(25, np.array([-100, 100, -200, 1])))

  # scene_objects.append(Cube(25, np.array([100/2, -100, -200, 1])))
  # scene_objects.append(Cube(25, np.array([-100/2, -100, -200, 1])))
  # scene_objects.append(Cube(25, np.array([100, -100, -200, 1])))
  # scene_objects.append(Cube(25, np.array([-100, -100, -200, 1])))

  scene = Scene(scene_objects, camera)

  root = Tk()

  canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='#1a1f1c')
  canvas.pack(fill=BOTH, expand=1)

  scene.update(canvas)

  root.mainloop()

  

