import os, yaml, util
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, ClearColor, Rectangle
from kivy.clock import Clock


class Valve:

  def __init__(self, pos):
    self.pos = pos
    self.modifier = 1
    
  def rotate_modifier(self):
    if self.modifier == -1:
      self.modifier = 1
    elif self.modifier == 1:
      self.modifier = -1
      
      
class Pump:

  def __init__(self, section):
    self.section = section
    self.power = 5.0
    self.modifier = 0
    
  def rotate_modifier(self):
    if self.modifier == 0:
      self.modifier = 1
    elif self.modifier == 1:
      self.modifier = -1
    elif self.modifier == -1:
      self.modifier = 0

      
class Section:

  def __init__(self, pos, pattern):
    self.pos = pos
    self.pattern = pattern
    self.content = 0.0
    self.capacity = 10.0
    self.neighbors = []
    
    
class PipeNetwork:

  def __init__(self, cells, cols, rows):
    self.cells = cells
    self.rows = rows
    self.cols = cols
    self.sections = []
    self.pumps = []
    self.valves = []
    self.build()

  def find_section(self, pos, pattern):
    for section in self.sections:
      if section.pos == pos and section.pattern == pattern:
        return section
    return None
    
  def join_vertical(self, pos, pos_top):
    section = self.find_section(pos, '1000')
    section_top = self.find_section(pos_top, '0010')
    if section != None and section_top != None:
      section.neighbors.append(section_top)
      section_top.neighbors.append(section)
      
  def join_horizontal(self, pos, pos_right):
    section = self.find_section(pos, '0100')
    section_right = self.find_section(pos_right, '0001')
    if section != None and section_right != None:
      section.neighbors.append(section_right)
      section_right.neighbors.append(section)
    
  def build(self):
    i_row = 0
    i_col = 0
    for i_row in range(self.rows):
      for i_col in range(self.cols):
        cell = self.cells[i_row][i_col]
        if cell.pattern == None:
          continue
        cell_sections = []
        if cell.pattern[0] == '1':
          cell_sections.append(Section([i_row, i_col], '1000'))
          self.sections.append(cell_sections[-1])
        if cell.pattern[1] == '1':
          cell_sections.append(Section([i_row, i_col], '0100'))
          self.sections.append(cell_sections[-1])
        if cell.pattern[2] == '1':
          cell_sections.append(Section([i_row, i_col], '0010'))
          self.sections.append(cell_sections[-1])
        if cell.pattern[3] == '1':
          cell_sections.append(Section([i_row, i_col], '0001'))
          self.sections.append(cell_sections[-1])
        if cell.type == 'pump':
          self.pumps.append(Pump(cell_sections[-1]))
        elif cell.addon == 'valve':
          self.valves.append(Valve([i_row, i_col]))
        for section in cell_sections:
          for neighbor in cell_sections:
            if neighbor != section:
              section.neighbors.append(neighbor)
    for i_row in range(self.rows):
      for i_col in range(self.cols):
        #cell = self.cells[i_row][i_col]
        if i_row < (self.rows - 1):
          #cell_top = self.cells[i_row + 1][i_col]
          self.join_horizontal([i_row, i_col], [i_row + 1, i_col])
        if i_col < (self.cols - 1):
          #cell_right = self.cells[i_row][i_col + 1]
          self.join_vertical([i_row, i_col], [i_row, i_col + 1])
          
  def search_section(self, section, searched):
    if section in searched:
      return
    else: searched.append(section)
    if section.content < section.capacity:
      return section, searched
    else:
      for neighbor in section.neighbors:
        if not neighbor in searched:
          return self.search_section(neighbor, searched)
          
  def valve_open(self, pos):
    for valve in self.valves:
      if valve.pos == pos:
        return valve.modifier == 1
    return True #no valve found to obstruct
          
  def search_fill(self, previous, current, searched, fluid):
    if fluid == 0: return
    if current in searched:
      return
    else: searched.append(current)
    if current.content < current.capacity:
      if previous == None:
        can_pass = True
      elif previous.pos != current.pos:
        can_pass = True
      else: can_pass = self.valve_open(current.pos)
      if can_pass:
        diff = current.capacity - current.content
        if fluid > diff:
          current.content = current.capacity
          fluid -= diff
        else:
          current.content += fluid
          fluid = 0
    else:
      for neighbor in current.neighbors:
        if not neighbor in searched:
          return self.search_fill(current, neighbor, searched, fluid)
  
  def fill_section(self, section, fluid):
    diff = section.capacity - section.content
    if fluid > diff:
      section.content = section.capacity
      return fluid - diff
    else:
      section.content += fluid
      return 0
    
  def run_pumps(self):
    for pump in self.pumps:
      if pump.modifier > 0:
        self.search_fill(None, pump.section, [], pump.power)
        #fluid = pump.power
        # while fluid > 0:
          
          # section, searched = self.search_section(pump.section, [])
          # print section.pos, [x.pos for x in searched]
          # if section is None:
            # print 'No section found'
            # return
          # fluid = self.fill_section(section, fluid)
      elif pump.modifier < 0:
        if pump.power > pump.section.content:
          pump.section.content = 0
        else: pump.section.content -= pump.power
        
  def propagation(self):
    for section in self.sections:
      for neighbor in section.neighbors:
        if neighbor.pos != section.pos:
          can_pass = True
        else: can_pass = self.valve_open(section.pos)
        if can_pass:
          diff = section.content - neighbor.content
          if abs(diff) > 0.1: #TODO viscosity
            section.content -= diff / 2
            neighbor.content += diff / 2

          
class Cell():

  def __init__(self):
    self.pattern = None
    self.type = None
    self.addon = None


class SimulGrid(FloatLayout):

  def __init__(self, **kwargs):
    super(SimulGrid, self).__init__(**kwargs)
    self.rows = None
    self.cols = None
    self.cell_width = None
    self.cell_height = None
    self.network = None
    self.cells = self.load_data()
    with self.canvas:
      Color(.2, .2, .2)
      self.rect = Rectangle(pos=self.pos, size=self.size)
    self.bind(pos=self.update_gfx)
    self.bind(size=self.update_gfx)
    
  def build_network(self):
    self.network = PipeNetwork(list(self.cells), self.rows, self.cols)
    
  def on_touch_down(self, touch):
    if not self.collide_point(touch.x, touch.y):
      return
    i_row = int( (touch.x - self.pos[0]) / self.cell_width )
    i_col = int( (touch.y - self.pos[1]) / self.cell_height )
    cell = self.cells[i_row][i_col]
    if cell.type == 'pump':
      for pump in self.network.pumps:
        if pump.section.pos == [i_row, i_col]:
          pump.rotate_modifier()
    if cell.addon == 'valve':
      for valve in self.network.valves:
        if valve.pos == [i_row, i_col]:
          valve.rotate_modifier()
      
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
    
  def load_data(self):
    if os.path.isfile('data/pipeline-grid.yaml'):
      stream = file('data/pipeline-grid.yaml', 'r')
      cells = yaml.load(stream)
      return list(cells)
    else: return None
    
  def draw_tiles(self, *args):
    self.canvas.clear()
    with self.canvas:
      # ground and pipes
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
      #fluid
      if self.network != None:
        Color(.1,.5,1.)
        for section in self.network.sections:
          cell_x = self.pos[0] + section.pos[0] * self.cell_width
          cell_y = self.pos[1] + section.pos[1] * self.cell_height
          fill = section.content / section.capacity
          if section.pattern == '1000':
            pos = [cell_x + self.cell_width / 2, cell_y + self.cell_height / 2]
            size = [self.cell_width * 0.1 * fill, self.cell_height / 2]
            pos = [pos[0] - size[0] / 2, pos[1]]
          if section.pattern == '0100':
            pos = [cell_x + self.cell_width / 2, cell_y + self.cell_height / 2]
            size = [self.cell_width / 2, self.cell_height * 0.1 * fill]
            pos = [pos[0], pos[1] - size[1] / 2]
          if section.pattern == '0010':
            pos = [cell_x + self.cell_width / 2, cell_y]
            size = [self.cell_width * 0.1 * fill, self.cell_height / 2]
            pos = [pos[0] - size[0] / 2, pos[1]]
          if section.pattern == '0001':
            pos = [cell_x, cell_y + self.cell_height / 2]
            size = [self.cell_width / 2, self.cell_height * 0.1 * fill]
            pos = [pos[0], pos[1] - size[1] / 2]
          Rectangle(pos=pos, size=size)
        Color(1,1,1)
        # pumps
        for pump in self.network.pumps:
          cell_x = self.pos[0] + pump.section.pos[0] * self.cell_width
          cell_y = self.pos[1] + pump.section.pos[1] * self.cell_height
          if pump.modifier > 0:
            Rectangle(source=os.path.join(util.dir_img, 'indicator-plus.png'),
                pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
          elif pump.modifier < 0:
            Rectangle(source=os.path.join(util.dir_img, 'indicator-minus.png'),
                pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
        # valves
        for valve in self.network.valves:
          cell_x = self.pos[0] + valve.pos[0] * self.cell_width
          cell_y = self.pos[1] + valve.pos[1] * self.cell_height
          if valve.modifier > 0:
            Rectangle(source=os.path.join(util.dir_img, 'indicator-plus.png'),
                pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
          elif valve.modifier < 0:
            Rectangle(source=os.path.join(util.dir_img, 'indicator-minus.png'),
                pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
      # addons
      for i_row in range(self.rows):
        for i_col in range(self.cols):
          cell_x = self.pos[0] + i_row * self.cell_width
          cell_y = self.pos[1] + i_col * self.cell_height
          cell = self.cells[i_row][i_col]
          if not cell.addon is None:
            Rectangle(source=os.path.join(util.dir_img, cell.addon + '.png'),
                pos=[cell_x, cell_y], size=[self.cell_width, self.cell_height])
  

class Simulator:
  running = False
  grid = None

  @staticmethod
  def set_grid(simulgrid):
    Simulator.grid = simulgrid
  
  @staticmethod
  def process(dt):
    if Simulator.grid != None:
      Simulator.grid.network.run_pumps()
      Simulator.grid.network.propagation()
      Simulator.grid.draw_tiles()
    return Simulator.running

  @staticmethod    
  def start(instance):
    Clock.schedule_interval(Simulator.process, 0.2)
    Simulator.running = True
    
  @staticmethod  
  def stop(instance):
    Simulator.running = False