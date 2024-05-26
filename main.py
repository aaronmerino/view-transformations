from camera import Camera
from cube import Cube
import numpy as np
import random
import keyboard
from pynput.mouse import Controller
from pynput import mouse


from tkinter import Tk, Canvas, Frame, BOTH


WIDTH = 1600
HEIGHT = 800

class Scene:
  def __init__(self, objects: list, camera: Camera):
    self.objects = objects
    self.camera = camera

    self.random = random.choice([1, 2, 3])

    self.prev_mouse_x = None
    self.control_cam = False
    self.paused = False

    self.box_rotation_mode = 'RANDOM'

    def on_click(x, y, button, pressed):
      if pressed:
        if root.winfo_rootx() <= x <= root.winfo_rootx() + root.winfo_width() and root.winfo_rooty() <= y <= root.winfo_rooty() + root.winfo_height():
          if self.control_cam:
            self.releaseCamera()
          else:
            if root.focus_get():
              self.enterCamera()

    listener = mouse.Listener(on_click=on_click)
    listener.start()


  def enterCamera(self):
    root.configure(cursor='none')
    self.control_cam = True

  def releaseCamera(self):
    root.configure(cursor='arrow')
    self.control_cam = False
    self.prev_mouse_x = None

  def render(self, canvas):
    for o in self.objects:
      o.render(camera, canvas)
        

  def update(self, canvas):
    global FOCAL_LENGTH

    mouse = Controller()

    if self.prev_mouse_x is None:
      self.prev_mouse_x = mouse.position
    else:
      if not (self.prev_mouse_x == mouse.position) and self.control_cam:
        
        mouse_difference = np.array(mouse.position) - np.array(self.prev_mouse_x)

        camera.rotate_y_axis(mouse_difference[0]*np.pi/1024)
        camera.rotate_bas_u_axis(-mouse_difference[1]*np.pi/1024)

        mouse.position = (root.winfo_x() + (root.winfo_width()//2), root.winfo_y() +  (root.winfo_height()//2))
        self.prev_mouse_x = (root.winfo_x() + (root.winfo_width()//2), root.winfo_y() + (root.winfo_height()//2))
          
    
    if root.focus_get():
      keyboard.start_recording()
      currently_pressed = dict(keyboard._pressed_events)
      
      for event in currently_pressed:
        print(event)
        if event == 1: # esc key
          self.control_cam = False
        if event == 2: # 1 key
          self.camera.setFocalLength(self.camera.getFocalLength() + 1)
        if event == 3: # 2 key
          self.camera.setFocalLength(self.camera.getFocalLength() - 1)
        if event == 4: # 3 key
          self.camera.setOrthographicCamera(True)
        if event == 5: # 4 key
          self.camera.setOrthographicCamera(False)
        
        if event == 19: # r key
          self.paused = False
        if event == 20: # t key
          self.paused = True
        if event == 21: # y key
          self.paused = True
          for o in self.objects:
            o.setBasis(np.array([np.array([1, 0, 0, 0]) , np.array([0, 1, 0, 0]), np.array([0, 0, 1, 0])]))
        if event == 22: # u key
          self.box_rotation_mode = 'RANDOM'
          self.paused = False
        if event == 23: # i key
          self.box_rotation_mode = 'X-AXIS'
          self.paused = False
        if event == 24: # o key
          self.box_rotation_mode = 'Y-AXIS'
          self.paused = False
        if event == 25: # p key
          self.box_rotation_mode = 'Z-AXIS'
          self.paused = False

        if event == 75: # key l_arrow
          camera.rotate_y_axis(-np.pi/256)
        if event == 77: # key r_arrow
          camera.rotate_y_axis(np.pi/256)
        if event == 72: # key up_arrow
          camera.rotate_bas_u_axis(np.pi/256)
        if event == 80: # key down_arrow
          camera.rotate_bas_u_axis(-np.pi/256)

        if event == 16: # key Q
          camera.translate(2*camera.v)    
        if event == 18: # key E
          camera.translate(-2*camera.v)  
        if event == 17: # key W
          camera.translate(-2*camera.w)
        if event == 30: # key A
          camera.translate(2*camera.u)
        if event == 31: # key S
          camera.translate(2*camera.w)
        if event == 32: # key D
          camera.translate(-2*camera.u)

      keyboard.stop_recording()
    
    # Clear the canvas
    canvas.delete("redraw")

    if not self.paused:
      for o in self.objects:
        if self.box_rotation_mode == 'RANDOM':
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
        elif self.box_rotation_mode == 'X-AXIS':
          o.rotate_x_axis(np.pi/256) 
        elif self.box_rotation_mode == 'Y-AXIS':
          o.rotate_y_axis(np.pi/256) 
        elif self.box_rotation_mode == 'Z-AXIS':
          o.rotate_z_axis(np.pi/256) 
        
    
    canvas.create_text(10, HEIGHT-30, text=f'focal length: {-self.camera.getFocalLength()}', fill="white", font=("Monaco", 8), anchor="nw", tag="redraw")
    canvas.create_text(10, HEIGHT-20, text=f'orthographic mode: {self.camera.getOrthographicMode()}', fill="#ff2500" if self.camera.getOrthographicMode() else "white", font=("Monaco", 8), anchor="nw", tag="redraw")

    self.render(canvas)

    root.after(1, self.update, canvas)  # Update every 10 ms

    

            
if __name__ == "__main__":


  camera = Camera(WIDTH, HEIGHT, WIDTH/2, HEIGHT/2, -300, -4000, np.array([0, 0, 200, 1]), np.array([0, 0, -1, 0]))

  scene_objects = []
  # scene_objects.append(Cube(1000, np.array([0, 0, -20000, 1])))

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

  scene_objects.append(Cube(25, np.array([100/2, -100/2, -200, 1])))
  scene_objects.append(Cube(25, np.array([-100/2, -100/2, -200, 1])))



  scene_objects.append(Cube(25, np.array([0, -200, 0, 1])))

  scene_objects.append(Cube(25, np.array([150, -200, 0, 1])))
  scene_objects.append(Cube(25, np.array([-150, -200, 0, 1])))
  scene_objects.append(Cube(25, np.array([0, -200, 150, 1])))
  scene_objects.append(Cube(25, np.array([0, -200, -150, 1])))

  scene_objects.append(Cube(25, np.array([100, -200, 0, 1])))
  scene_objects.append(Cube(25, np.array([-100, -200, 0, 1])))
  scene_objects.append(Cube(25, np.array([0, -200, 100, 1])))
  scene_objects.append(Cube(25, np.array([0, -200, -100, 1])))

  scene_objects.append(Cube(25, np.array([50, -200, 0, 1])))
  scene_objects.append(Cube(25, np.array([-50, -200, 0, 1])))
  scene_objects.append(Cube(25, np.array([0, -200, 50, 1])))
  scene_objects.append(Cube(25, np.array([0, -200, -50, 1])))

  scene_objects.append(Cube(25, np.array([50, -200, 50, 1])))
  scene_objects.append(Cube(25, np.array([-50, -200, 50, 1])))

  scene_objects.append(Cube(25, np.array([50, -200, -50, 1])))
  scene_objects.append(Cube(25, np.array([-50, -200, -50, 1])))






  scene = Scene(scene_objects, camera) 

  root = Tk()
  root.resizable(False, False)

  root.bind('<FocusOut>', lambda event: scene.releaseCamera())

  canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='#1a1f1c')
  canvas.pack(fill=BOTH, expand=1)
  # List of controls
  controls = [
      "ESC - gain back mouse control",
      "CLICK - toggle mouse camera control",
      "R - resume cube rotation",
      "T - pause cube rotation",
      "Y - cubes reset rotation",
      "U - cubes random rotation",
      "I - cubes rotate in x-axis",
      "O - cubes rotate in y-axis",
      "P - cubes rotate in z-axis",

      "1 - decrease focal length",
      "2 - increase focal length",
      "3 - set orthographic mode on",
      "4 - set orthographic mode off",
      "W - move forward",
      "A - move left",
      "S - move backward",
      "D - move right",
      "Q - move up",
      "E - move down",
      "ARROW_KEYS - aim camera"
  ]

  # Add each control as a separate line of text
  for i, control in enumerate(controls):
      canvas.create_text(10, 10 + i * 20, text=control, fill="white", font=("Monaco", 8), anchor="nw")

  scene.update(canvas)

  root.mainloop()

  

