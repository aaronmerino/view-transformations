import numpy as np

class Camera:
  # nx = picture plane's # of pixels along row
  # ny = picture plane's # of pixels along height
  def __init__(self, nx=400, ny=400, left=200, bottom=200, near=-100, far=-400, origin=np.array([0, 0, 0, 1]), view_dir=np.array([0, 0, -1, 0])):
    self.orthographic = False
    self.nx = int(nx)
    self.ny = int(ny)

    self.left = int(left)
    self.bottom = int(bottom)

    self.right = -left
    self.top = -bottom

    self.near = int(near)
    self.far = int(far)

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
  
  def convert_xyz_to_uvw(self, point):
    R_translate = np.array([  [1, 0, 0, -self.origin[0]],
                              [0, 1, 0, -self.origin[1]],
                              [0, 0, 1, -self.origin[2]],
                              [0, 0, 0, 1]])
    R_uvw = np.array([  self.u,
                        self.v,
                        self.w,
                        [0, 0, 0, 1]])
    
    R_full = np.dot(R_uvw, R_translate)

    return np.dot(R_full, point)
  

  def getOrthographicMode(self):
    return self.orthographic
  
  def setOrthographicCamera(self, x=False):
    self.orthographic = x

  def getFocalLength(self):
    return self.near

  def setFocalLength(self, fl):
    if fl >= 0:
      return
    
    self.near = int(fl)

  def getViewingTransformation(self):
    M_vp = np.array([[self.nx/2,    0,   0, (self.nx - 1)/2],
                          [  0,  self.ny/2,   0, (self.ny - 1)/2],
                          [  0,     0,   1,          0],
                          [  0,     0,   0,          1]])
  
    M_orth = np.array([[2/(self.right - self.left),                             0,                          0, -1*(self.right + self.left)/(self.right - self.left)],
                          [                           0,    2/(self.top - self.bottom),                          0, -1*(self.top + self.bottom)/(self.top - self.bottom)],
                          [                           0,                             0,   2/(self.near - self.far), -1*(self.near + self.far)/(self.near - self.far)],
                          [                           0,                             0,                          0,  1]])
    
    M_cam = np.dot(np.array([self.u,
                                  self.v,
                                  self.w,
                                  [  0,   0,   0, 1]]), np.array([[  1,   0,   0, -self.origin[0]],
                                                                  [  0,   1,   0, -self.origin[1]],
                                                                  [  0,   0,   1, -self.origin[2]],
                                                                  [  0,   0,   0, 1]]))
    
    M_p = np.array([[self.near,     0,            0,         0],
                          [  0,  self.near,            0,         0],
                          [  0,     0,   self.near + self.far, -self.far*self.near],
                          [  0,     0,            1,         0]])

    M_full = np.dot(M_vp, np.dot(M_orth, np.dot(M_p, M_cam)))

    if self.orthographic:
      M_full = np.dot(M_vp, np.dot(M_orth, M_cam))

    return M_full

  def rotate_y_axis(self, deg):
    M_rotate_y = np.array([[np.cos(deg),    0,     np.sin(deg), 0],
                          [           0,    1,               0, 0],
                          [-np.sin(deg),    0,     np.cos(deg), 0],
                          [            0,   0,               0, 1]])
    
    self.u = np.dot(M_rotate_y, self.u)      
    self.v = np.dot(M_rotate_y, self.v)  
    self.w = np.dot(M_rotate_y, self.w)  

    self.u = self.u/np.linalg.norm(self.u)
    self.v = self.v/np.linalg.norm(self.v)
    self.w = self.w/np.linalg.norm(self.w)

  def rotate_bas_u_axis(self, deg):
    w = self.u
    u_cross = np.cross(self.up_dir[:3], w[:3])
    u_cross = np.append(u_cross, 0)

    u = u_cross/np.linalg.norm(u_cross)

    v_cross = np.cross(w[:3], u[:3])
    v_cross = np.append(v_cross, 0)
    v = v_cross
  

    R_uvw = np.array([  u,
                        v,
                        w,
                        [0, 0, 0, 1]])
    
    M_rotate_z = np.array([[np.cos(deg), -np.sin(deg), 0, 0],
                          [ np.sin(deg),  np.cos(deg), 0, 0],
                          [           0,            0, 1, 0],
                          [            0,           0, 0, 1]])
    
    M_full = np.dot(R_uvw.T, np.dot(M_rotate_z, R_uvw))
    

    self.u = np.dot(M_full, self.u)      
    self.v = np.dot(M_full, self.v)  
    self.w = np.dot(M_full, self.w)  

    self.u = self.u/np.linalg.norm(self.u)
    self.v = self.v/np.linalg.norm(self.v)
    self.w = self.w/np.linalg.norm(self.w)

  def translate(self, vector):
    M_translate = np.array([[1, 0, 0, vector[0]],
                            [0, 1, 0, vector[1]],
                            [0, 0, 1, vector[2]],
                            [0, 0, 0,       1]])
    
    self.origin = np.dot(M_translate, self.origin)