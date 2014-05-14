max_values = { 'bool': 1, 'word': 255, 'dword': 65535}


class Variable:

  def __init__(self, name, type, text='', value=None):
    self.name = name
    self.type = type
    self.text = text
    self.value = value
    self.bindings = []
    self.meta = dict()
    
  def set_value(self, value):
    if self.value != value:
      self.value = value
      self.notify('value')
      
  def set_text(self, text):
    if self.text != text:
      self.text = text
      self.notify('text')
    
  def notify(self, attr_name):
    for binding in self.bindings:
      if binding.source_attr == attr_name:
        binding.update(getattr(self, attr_name))
        
  def get_bounds(self):
    if 'min' in self.meta:
      min_val = self.meta['min']
    else: min_val = 0
    if 'max' in self.meta:
      max_val = self.meta['max']
    else: max_val = max_values[self.type]
    return min_val, max_val
    