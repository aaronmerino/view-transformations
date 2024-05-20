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

  def render(self, camera):
    M = camera.getViewingTransformation()
    transformed_vertices = np.array([np.dot(M, vertex) for vertex in self.vertices])

    return transformed_vertices

  def rotate_x_axis(self, deg):
    return
  
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

  def rotate_z_axis(self, deg):
    return
  
  def rotate_axis(self, vec, deg):
    return