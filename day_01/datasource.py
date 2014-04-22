class DataSource:
  def __init__(self, mode=None):
    self.mode = mode
    
  def read(name):
    if mode == 'offline':
      vartype = variables[name].type
      if vartype == 'bool':
        return randint(0, 1)
      elif vartype == 'word':
        return randint(0, 255)
      elif vartype == 'dword':
        return randint(0, 65535)
      elif vartype == 'string':
        return randomword(16)
    elif mode == 'online':
      pass
      # TODO opc connection
      
  def write(name):
    if mode == 'offline':
      pass
    elif mode == 'online':
      # TODO opc connection
      pass
  
