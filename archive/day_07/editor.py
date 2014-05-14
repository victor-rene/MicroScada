import os
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from util import dirname


class Cell():
  def __init__(self):
    self.pattern = None
    self.type = None
    self.addon = None

class Grid(FloatLayout):
  def __init__(self, **kwargs):
    super(Grid, self).__init__(**kwargs)
    self.rows = None
    self.cols = None
    self.cell_width = None
    self.cell_height = None
    self.cells = None
    with self.canvas:
      Color(.2, .2, .2)
      self.rect = Rectangle(pos=self.pos, size=self.size)
    self.bind(pos=self.update_gfx)
    self.bind(size=self.update_gfx)
    
  def on_touch_down(self, touch):
    if not self.collide_point(touch.x, touch.y):
      return
    i_row = int( (touch.x - self.pos[0]) / self.cell_width )
    i_col = int( (touch.y - self.pos[1]) / self.cell_height )
    cell = self.cells[i_row][i_col]
    if Editor.mode == 'pipe-i':
      cell.type = 'pipe'
      cell.pattern = '1010'
    elif Editor.mode == 'pipe-x':
      cell.type = 'pipe'
      cell.pattern = '1111'
    elif Editor.mode == 'pipe-l':
      cell.type = 'pipe'
      cell.pattern = '1100'
    elif Editor.mode == 'pipe-t':
      cell.type = 'pipe'
      cell.pattern = '1110'
    elif Editor.mode == 'pump':
      cell.type = 'pump'
      cell.pattern = '1000'
    elif Editor.mode == 'valve':
      cell.addon = 'valve'
    elif Editor.mode == 'flowmeter':
      if cell.type == 'pipe' and cell.pattern.count('1') == 2:
        cell.addon = 'flowmeter'
    elif Editor.mode == 'turn-left':
      if not cell.pattern is None:
        cell.pattern = cell.pattern[-3:] + cell.pattern[0]
    elif Editor.mode == 'turn-right':
      if not cell.pattern is None:
        cell.pattern = cell.pattern[-1] + cell.pattern[:-1]
    elif Editor.mode == 'clear':
      cell.type = None
      cell.pattern = None
      cell.addon = None
    if Editor.mode != None:
      self.draw_tiles()
      
  def set_dimenstion(self, rows, cols):
    self.rows = rows
    self.cols = cols
    self.cells = [[Cell() for x in range(rows)] for y in xrange(cols)] 
    self.update_gfx()
    
  def update_gfx(self, *args):
    self.rect.pos = self.pos
    self.rect.size = self.size
    self.cell_width = self.size[0] / self.cols
    self.cell_height = self.size[1] / self.rows
    self.draw_tiles()
    
  def draw_tiles(self):
    self.canvas.clear()
    with self.canvas:
      self.rect = Rectangle(source=os.path.join(dirname, 'img', 'ground.png'),
          pos=self.pos, size=self.size)
      for i_row in range(self.rows):
        for i_col in range(self.cols):
          cell_x = self.pos[0] + i_row * self.cell_width
          cell_y = self.pos[1] + i_col * self.cell_height
          Rectangle(source=os.path.join(dirname, 'img', 'ground.png'),
              pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
          cell = self.cells[i_row][i_col]
          if not cell.pattern is None:
            Rectangle(source=os.path.join(dirname, 'img', cell.type + '-' + cell.pattern + '.png'),
                pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
          if not cell.addon is None:
            Rectangle(source=os.path.join(dirname, 'img', cell.addon + '.png'),
                pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
  

class Editor:
  mode = None
  @staticmethod
  def pipe_i(cls):
    Editor.mode = 'pipe-i'
  @staticmethod
  def pipe_l(self):
    Editor.mode = 'pipe-l'
  @staticmethod
  def pipe_t(self):
    Editor.mode = 'pipe-t'
  @staticmethod
  def pipe_x(self):
    Editor.mode = 'pipe-x'
  @staticmethod
  def valve(self):
    Editor.mode = 'valve'
  @staticmethod
  def pump(self):
    Editor.mode = 'pump'
  @staticmethod
  def flowmeter(self):
    Editor.mode = 'flowmeter'
  @staticmethod
  def turn_left(self):
    Editor.mode = 'turn-left'
  @staticmethod
  def turn_right(self):
    Editor.mode = 'turn-right'
  @staticmethod
  def clear(self):
    Editor.mode = 'clear'
