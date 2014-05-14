import os
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color
from datamgr import variables
from util import dirname
from variable import max_values


class Binding:

  def __init__(self, source, source_attr, target, target_attr):
    self.source = source
    self.source_attr = source_attr
    self.target = target
    self.target_attr = target_attr
    
  def update(self, new_value):
    if 'bounds' in self.source.meta:
      scale_min = self.source.meta['bounds'][0]
      scale_max = self.source.meta['bounds'][1]
    else:
      scale_min = 0
      scale_max = max_values[self.source.type]
    scale = float(self.source.value - scale_min) / (scale_max - scale_min)
    print self.source.value, scale_min, scale_max, scale
    self.target.level = scale * self.target.level_max
    self.target.update_rect()
      

class Thermometer(GridLayout):

  def __init__(self, **kwargs):
    super(Thermometer, self).__init__(**kwargs)
    self.cols = 1
    self.rows = 1
    self.level_max = 0.7
    self.level = 0
    with self.canvas:
      self.rect = Rectangle(source=os.path.join(dirname, 'img', 'thermometer.png'), pos=self.pos, size=self.size)
      Color(0.65, 0, 0)
      self.mercury = Rectangle(pos=self.pos, size=[self.size[0] / 4, self.size[1]])
    self.bind(pos=self.update_rect)
    self.bind(size=self.update_rect)
    
  def update_rect(self, *args):
    self.rect.pos = self.pos
    self.rect.size = self.size
    x = self.pos[0] + self.size[0] / 2 - self.size[0] / 8
    y = self.pos[1] + self.size[1] * 0.25
    self.mercury.pos = [x, y]
    self.mercury.size = size=[self.size[0] / 4, self.size[1] * self.level]
      
  def set_var(self, name):
    variable = variables[name]
    binding = Binding(variable, 'value', self, None)
    variable.bindings.append(binding)