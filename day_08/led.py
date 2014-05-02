import os
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from datamgr import variables
from util import dirname


class Binding:

  def __init__(self, source, source_attr, target, target_attr):
    self.source = source
    self.source_attr = source_attr
    self.target = target
    self.target_attr = target_attr
    
  def update(self, new_value):
    dirname = os.path.dirname(os.path.realpath(__file__))
    if self.source.value == 1:
      self.target.source = os.path.join(dirname, 'img', 'led_green.png')
    elif self.source.value == 0:
      self.target.source = os.path.join(dirname, 'img', 'led_red.png')

class Led(GridLayout):

  def __init__(self, **kwargs):
    super(Led, self).__init__(**kwargs)
    self.cols = 1
    self.rows = 1
    self.image = Image(source = os.path.join(dirname, 'img', 'led_red.png'), pos=self.pos, size=self.size)
    self.add_widget(self.image)
    self.bind(pos=self.update_img)
    self.bind(size=self.update_img)
      
  def set_var(self, name):
    variable = variables[name]
    binding = Binding(variable, 'value', self.image, None)
    variable.bindings.append(binding)
    
  def update_img(self, *args):
    self.image.pos = self.pos
    self.image.size = self.size