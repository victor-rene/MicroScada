from random import randint


class DataSource:

  def __init__(self, mode=None):
    self.mode = mode
    
  def read(self, variable):
    if self.mode == 'offline':
      if variable.type == 'bool':
        return randint(0, 1)
      elif variable.type == 'word':
        return randint(0, 255)
      elif variable.type == 'dword':
        return randint(0, 65535)
      elif variable.type == 'string':
        return randomword(16)
    elif mode == 'online':
      pass
      # TODO opc connection
      
  def write(self, name):
    if mode == 'offline':
      pass
    elif mode == 'online':
      # TODO opc connection
      pass
  
