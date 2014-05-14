import os, util
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class Junction:

  def __init__(self, sections, addon):
    self.sections = []
    self.addon = addon
    
    
class Section:

  def __init__(self, capacity, endpoints):
    self.content = 0
    self.capacity = capaticty
    self.endpoints = endpoints
    self.neighbors = []
    
class Pump:

  def __init__(self, value=0, pos, pattern):
    self.value = value
    self.pos = pos
    self.pattern = pattern
    
    
class Valve:

  def __init__(self, value=0):
    self.value = value
    

def get_vector(pos1, pos2):
  return [pos1[0] - pos2[0], pos1[1] - pos2[1]]
    
def get_vertors(pattern):
  vectors = []
  if pattern[0] == '1':
    vectors.append([0, 1])
  if pattern[1] == '1':
    vectors.append([1, 0])
  if pattern[2] == '1':
    vectors.append([0, -1])
  if pattern[3] == '1':
    vectors.append([-1, 0])
  return vectors
  
def apply_vector(pos, vector)
  return [pos[0] + vector[0], pos[1] + vector[1]]
    
    
class Network:

  def __init__(self):
    self.grid = None
    self.pumps = []
    self.trades = []
    self.sections = []
    self.explored = []
    self.zones = []

  def valid_zone(zone):
    return (zone[0] >= 0 and zone[0] < grid.rows
        and zone[1] >= 0 and zone[1] < grid.cols)
    
  def explore(zone):
    if zone if self.explored:
      return
    self.explored.append(zone)
    cell = self.grid.cells[zone[0]][zone[1]]
    if not cell.pattern is None:
      self.zones.append(zone)
      vectors = get_vertors(cell.pattern)
    local_sections = []
    for vector in vectors:
      adj_zone = apply_vector(zone, vector)
      if not valid_zone(adj_zone):
        continue
      section = Section(10, [zone, adj_zone])
      self.sections.append(section)
      local_sections.append(section)
      explore(adj_zone)
    for section in local_sections:
      for neighbor in local_sections:
        if neighbor != section:
          section.neighbors.append(neighbor)
          
  def join_zones():
    for zone if self.zones:
      
  def is_closed:
    return len(self.zones) == len(self.explored)
    
  def build(self, grid):
    self.grid = grid
    i_row = 0
    i_col = 0
    for i_row in grid.rows:
      for i_col in grid.cols:
        cell = grid.cells[i_row][i_col]
        if cell.type == 'pump':
          pump = Pump(0, [i_row, i_col], cell.pattern)
          pumps.append(pump)
    if len(pumps) > 0:
      explore(pumps[0].pos)
      

class Cell():

  def __init__(self):
    self.pattern = None
    self.type = None
    self.addon = None

class SimulGrid(FloatLayout):

  def __init__(self, **kwargs):
    super(EditGrid, self).__init__(**kwargs)
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
      self.rect = Rectangle(source=os.path.join(util.dirname, 'img', 'ground.png'),
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
  

class Simulator:

  mode = None
  
  @staticmethod
  def start(cls):
    Simulator.mode = 'pipe-i'
    
  @staticmethod
  def stop(cls):
    Simulator.mode = 'pipe-l'
    
  @staticmethod
  def reset(self):
    Simulator.mode = 'pipe-t'
    
  @staticmethod
  def setup(self):
    Simulator.mode = 'pipe-x'