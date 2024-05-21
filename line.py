import numpy as np

class Line:
  def __init__(self, A, B):
    self.A = A
    self.B = B

  def getVertices(self):
    return [self.A, self.B]