import numpy as np

class Vasicek:
  
  def __init__(self):
    pass

  def set_param(self, dt: float, a: float, b: float, sigma: float):
    self.dt = dt
    self.a = a
    self.b = b
    self.sigma = sigma

  def gen_scen(self, r0: float, n: int, t: float, random_state: str = 0) -> np.ndarray:
    m = int(t/self.dt)
    r = np.zeros([m+1, n])
    r[0] = r0
    np.random.seed(random_state)
    dW = np.random.normal(0, np.sqrt(self.dt), [m, n])
    for i in range(m):
      r[i+1] = r[i] + self.a*(self.b-r[i])*self.dt + self.sigma*dW[i]
    return r


# if __name__ == '__main__':
#   dt = 1/12
#   a = 0.3
#   b = 0.04
#   sigma = 0.25

#   r0 = 0.01
#   n = 20
#   t = 100

#   vas = Vasicek()
#   vas.set_param(dt, a, b, sigma)
#   vas.gen_scen(r0, n, t)
  
