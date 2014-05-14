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
    