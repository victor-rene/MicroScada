import os
import math
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color, Line
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
    self.target.angle = scale * (self.target.angle_max - self.target.angle_min) + self.target.angle_min
    self.target.update_rect()
      

class Manometer(GridLayout):

  def __init__(self, **kwargs):
    super(Manometer, self).__init__(**kwargs)
    self.cols = 1
    self.rows = 1
    self.angle_min = 3.927
    self.angle_max = -0.785
    self.angle = 1.571
    with self.canvas:
      self.rect = Rectangle(source=os.path.join(dirname, 'img', 'manometer.png'), pos=self.pos, size=self.size)
      Color(.1, .1, .1)
      middle_x = self.pos[0] + self.size[0] / 2
      middle_y = self.pos[1] + self.size[1] / 2
      tip_x = (math.cos(self.angle) * 0.4 * self.size[0]) + middle_x
      tip_y = (math.sin(self.angle) * 0.4 * self.size[1]) + middle_y
      self.needle = Line(points=[middle_x, middle_y, tip_x, tip_y], width=2)
    self.bind(pos=self.update_rect)
    self.bind(size=self.update_rect)
    
  def update_rect(self, *args):
    self.rect.pos = self.pos
    self.rect.size = self.size
    middle_x = self.pos[0] + self.size[0] / 2
    middle_y = self.pos[1] + self.size[1] / 2
    tip_x = (math.cos(self.angle) * 0.4 * self.size[0]) + middle_x
    tip_y = (math.sin(self.angle) * 0.4 * self.size[1]) + middle_y
    self.needle.points = [middle_x, middle_y, tip_x, tip_y]
      
  def set_var(self, name):
    variable = variables[name]
    binding = Binding(variable, 'value', self, None)
    variable.bindings.append(binding)