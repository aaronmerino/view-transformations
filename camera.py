import numpy as np

class Camera:
  # nx = picture plane's # of pixels along row
  # ny = picture plane's # of pixels along height
  def __init__(self, nx=400, ny=400, left=100, bottom=100, near=-100, far=-400, origin=np.array([0, 0, 0, 1]), view_dir=np.array([0, 0, -1, 0])):
    self.nx = nx
    self.ny = ny

    self.left = left
    self.bottom = bottom

    self.right = -left
    self.top = -bottom

    self.near = near    
    self.far = far

    self.origin = origin    # in terms of world space
    self.view_dir = view_dir
    self.up_dir = np.array([0, 1, 0, 0])

    self.w = (-1 * view_dir)/np.linalg.norm(view_dir)
    u_cross = np.cross(self.up_dir[:3], self.w[:3])
    u_cross = np.append(u_cross, 0)

    self.u = u_cross/np.linalg.norm(u_cross)

    v_cross = np.cross(self.w[:3], self.u[:3])
    v_cross = np.append(v_cross, 0)
    self.v = v_cross




    # Viewport Transformation
    self.M_vp = np.array([[nx/2,    0,   0, (nx - 1)/2],
                          [  0,  ny/2,   0, (ny - 1)/2],
                          [  0,     0,   1,          0],
                          [  0,     0,   0,          1]])
  
    self.M_orth = np.array([[2/(self.right - self.left),                             0,                          0, -1*(self.right + self.left)/(self.right - self.left)],
                          [                           0,    2/(self.top - self.bottom),                          0, -1*(self.top + self.bottom)/(self.top - self.bottom)],
                          [                           0,                             0,   2/(self.near - self.far), -1*(self.near + self.far)/(self.near - self.far)],
                          [                           0,                             0,                          0,  1]])
    
    self.M_cam = np.dot(np.array([self.u,
                                  self.v,
                                  self.w,
                                  [  0,   0,   0, 1]]), np.array([[  1,   0,   0, -self.origin[0]],
                                                                  [  0,   1,   0, -self.origin[1]],
                                                                  [  0,   0,   1, -self.origin[2]],
                                                                  [  0,   0,   0, 1]]))
    
    self.M_p = np.array([[near,     0,            0,         0],
                          [  0,  near,            0,         0],
                          [  0,     0,   near + far, -far*near],
                          [  0,     0,            1,         0]])

    self.M_full = np.dot(self.M_vp, np.dot(self.M_orth, np.dot(self.M_p, self.M_cam)))

  
  def getViewingTransformation(self):
    return self.M_full