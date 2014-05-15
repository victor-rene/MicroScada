import os, util
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
# from kivy.uix.popup import Popup
# from variableselector import VariableSelector
from datamgr import variables


class Binding:

  def __init__(self, source, source_attr, target, target_attr):
    self.source = source
    self.source_attr = source_attr
    self.target = target
    self.target_attr = target_attr
    
  def update(self, new_value):
    if self.source.value == 1:
      self.target.source = os.path.join(util.dir_img, 'led_green.png')
    elif self.source.value == 0:
      self.target.source = os.path.join(util.dir_img, 'led_red.png')

      
class Led(GridLayout):

  def __init__(self, **kwargs):
    super(Led, self).__init__(**kwargs)
    self.cols = 1
    self.rows = 1
    self.image = Image(source = os.path.join(util.dir_img, 'led_red.png'), pos=self.pos, size=self.size)
    self.add_widget(self.image)
    self.bind(pos=self.update_img)
    self.bind(size=self.update_img)
    self.variable = None
      
  def set_var(self, name):
    self.variable = variables[name]
    binding = Binding(self.variable, 'value', self.image, None)
    self.variable.bindings.append(binding)
    
  def update_img(self, *args):
    self.image.pos = self.pos
    self.image.size = self.size