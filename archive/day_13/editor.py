import os, yaml, util
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class Cell():
  def __init__(self):
    self.pattern = None
    self.type = None
    self.addon = None

class EditGrid(FloatLayout):
  def __init__(self, **kwargs):
    super(EditGrid, self).__init__(**kwargs)
    self.rows = None
    self.cols = None
    self.cell_width = None
    self.cell_height = None
    self.cells = self.load_data()
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
      if not cell.type is None:
        if cell.addon == 'valve':
          cell.addon = None
        else: cell.addon = 'valve'
    elif Editor.mode == 'flowmeter':
      if cell.type == 'pipe' and cell.pattern.count('1') == 2:
        if cell.addon == 'flowmeter':
          cell.addon = None
        else: cell.addon = 'flowmeter'
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
      self.save_data()
      self.draw_tiles()
      
  def set_dimenstion(self, rows, cols):
    self.rows = rows
    self.cols = cols
    if self.cells is None:
      self.cells = [[Cell() for x in range(rows)] for y in xrange(cols)]
    self.update_gfx()
    
  def update_gfx(self, *args):
    self.cell_width = self.size[0] / self.cols
    self.cell_height = self.size[1] / self.rows
    self.draw_tiles()
    
  def save_data(self):
    stream = file('data/pipeline-grid.yaml', 'w')
    yaml.dump(self.cells, stream)
    
  def load_data(self):
    if os.path.isfile('data/pipeline-grid.yaml'):
      stream = file('data/pipeline-grid.yaml', 'r')
      cells = yaml.load(stream)
      return list(cells)
    else: return None
    
  def draw_tiles(self, *args):
    self.canvas.clear()
    with self.canvas:
      Color(1,1,1,1)
      for i_row in range(self.rows):
        for i_col in range(self.cols):
          cell_x = self.pos[0] + i_row * self.cell_width
          cell_y = self.pos[1] + i_col * self.cell_height
          Rectangle(source=os.path.join(util.dir_img, 'ground.png'),
              pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
          cell = self.cells[i_row][i_col]
          if not cell.pattern is None:
            Rectangle(source=os.path.join(util.dir_img, cell.type + '-' + cell.pattern + '.png'),
                pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
          if not cell.addon is None:
            Rectangle(source=os.path.join(util.dir_img, cell.addon + '.png'),
                pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
  

class Editor:
  mode = None
  
  @classmethod
  def pipe_i(cls):
    cls.mode = 'pipe-i'
    
  @classmethod
  def pipe_l(cls):
    cls.mode = 'pipe-l'
    
  @classmethod
  def pipe_t(cls):
    cls.mode = 'pipe-t'
    
  @classmethod
  def pipe_x(cls):
    cls.mode = 'pipe-x'
    
  @classmethod
  def valve(cls):
    cls.mode = 'valve'
    
  @classmethod
  def pump(cls):
    cls.mode = 'pump'
    
  @classmethod
  def flowmeter(cls):
    cls.mode = 'flowmeter'
    
  @classmethod
  def turn_left(cls):
    cls.mode = 'turn-left'
    
  @classmethod
  def turn_right(cls):
    cls.mode = 'turn-right'
    
  @classmethod
  def clear(cls):
    cls.mode = 'clear'