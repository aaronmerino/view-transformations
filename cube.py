from line import Line
import numpy as np
import math

class Cube:
  def __init__(self, width=100, origin=np.array([0, 0, 0, 1])):
    self.width = width
    self.origin = origin    # in terms of world space

    # the homogeneus coordinate is 0 since these are vectors
    # basis vectors
    self.bas_x = np.array([1, 0, 0, 0])      # in terms of world space
    self.bas_y = np.array([0, 1, 0, 0])
    self.bas_z = np.array([0, 0, 1, 0])

    self.basis = np.array([self.bas_x, self.bas_y, self.bas_z])

    self.vertices = self._define_vertices()
    self.edges = self._define_edges()

  def _define_vertices(self):
    # Create an array to hold the vertices
    vertices = np.zeros((8, 4))

    # Calculate the half-width
    half_width = self.width / 2

    # Define the 8 vertices

    vertices[0] = self.origin + (self.basis[0]  + self.basis[1] + self.basis[2]) * (self.width - half_width)
    vertices[1] = self.origin + (self.basis[0]  + self.basis[1] - self.basis[2]) * (self.width - half_width)

    vertices[2] = self.origin + (self.basis[0]  - self.basis[1] + self.basis[2]) * (self.width - half_width)
    vertices[3] = self.origin + (self.basis[0]  - self.basis[1] - self.basis[2]) * (self.width - half_width)

    vertices[4] = self.origin + (-self.basis[0]  + self.basis[1] + self.basis[2]) * (self.width - half_width)
    vertices[5] = self.origin + (-self.basis[0]  + self.basis[1] - self.basis[2]) * (self.width - half_width)

    vertices[6] = self.origin + (-self.basis[0]  - self.basis[1] + self.basis[2]) * (self.width - half_width)
    vertices[7] = self.origin + (-self.basis[0]  - self.basis[1] - self.basis[2]) * (self.width - half_width)

    return vertices

  def _define_edges(self):
    edges = []

    edges.append(Line(self.vertices[0], self.vertices[1]))
    edges.append(Line(self.vertices[2], self.vertices[3]))
    edges.append(Line(self.vertices[4], self.vertices[5]))
    edges.append(Line(self.vertices[6], self.vertices[7]))

    edges.append(Line(self.vertices[0], self.vertices[2]))
    edges.append(Line(self.vertices[4], self.vertices[6]))
    edges.append(Line(self.vertices[2], self.vertices[6]))

    edges.append(Line(self.vertices[3], self.vertices[1]))
    edges.append(Line(self.vertices[3], self.vertices[7]))
    edges.append(Line(self.vertices[7], self.vertices[5]))
    edges.append(Line(self.vertices[1], self.vertices[5]))
    edges.append(Line(self.vertices[0], self.vertices[4]))
    

    return edges

  def render(self, camera, canvas):
    M = camera.getViewingTransformation()
    
    for e in self.edges:
      transformed_vertices = np.array([np.dot(M, vertex) for vertex in e.getVertices()])

      v_1 = transformed_vertices[0]
      v_2 = transformed_vertices[1]
      
      w_1 = v_1[3]
      i_1 = v_1[0]/w_1
      j_1 = v_1[1]/w_1

      w_2 = v_2[3]
      i_2 = v_2[0]/w_2
      j_2 = v_2[1]/w_2
      # apply pixel_color to canvas at position (i_2, j_2)
      # pixel_color_hex = "#%02x%02x%02x" % (int(min(0.5*255, 255)), int(min(0.5*255, 255)), int(min(0.5*255, 255)))

      # canvas.create_rectangle(i_2-1, j_2-1, i_2+1, j_2+1, outline="", fill=pixel_color_hex)
      line_color_hex = "#%02x%02x%02x" % (int(min(0.5*255, 255)), int(min(0.5*255, 255)), int(min(0.5*255, 255)))
      canvas.create_line(i_1, j_1, i_2, j_2, fill=line_color_hex)


  def rotate_x_axis(self, deg):
    M_rotate_x = np.array([[1,            0,            0, 0],
                          [ 0,  np.cos(deg), -np.sin(deg), 0],
                          [ 0,  np.sin(deg),  np.cos(deg), 0],
                          [ 0,            0,            0, 1]])
    
    self.bas_x = np.dot(M_rotate_x, self.basis[0])      
    self.bas_y = np.dot(M_rotate_x, self.basis[1])  
    self.bas_z = np.dot(M_rotate_x, self.basis[2])  

    self.basis = np.array([self.bas_x, self.bas_y, self.bas_z])

    self.vertices = self._define_vertices()
    self.edges = self._define_edges()
  
  def rotate_y_axis(self, deg):
    M_rotate_y = np.array([[np.cos(deg),    0,     np.sin(deg), 0],
                          [           0,    1,               0, 0],
                          [-np.sin(deg),    0,     np.cos(deg), 0],
                          [            0,   0,               0, 1]])
    
    self.bas_x = np.dot(M_rotate_y, self.basis[0])      
    self.bas_y = np.dot(M_rotate_y, self.basis[1])  
    self.bas_z = np.dot(M_rotate_y, self.basis[2])  

    self.basis = np.array([self.bas_x, self.bas_y, self.bas_z])

    self.vertices = self._define_vertices()
    self.edges = self._define_edges()

  def rotate_z_axis(self, deg):
    M_rotate_z = np.array([[np.cos(deg), -np.sin(deg), 0, 0],
                          [ np.sin(deg),  np.cos(deg), 0, 0],
                          [           0,            0, 1, 0],
                          [            0,           0, 0, 1]])
    
    self.bas_x = np.dot(M_rotate_z, self.basis[0])      
    self.bas_y = np.dot(M_rotate_z, self.basis[1])  
    self.bas_z = np.dot(M_rotate_z, self.basis[2])  

    self.basis = np.array([self.bas_x, self.bas_y, self.bas_z])

    self.vertices = self._define_vertices()
    self.edges = self._define_edges()
  
  def rotate_axis(self, vec, deg):
    return