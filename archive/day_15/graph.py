import util
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Line
from datamgr import datastr, variables


class Graph(FloatLayout):

  def __init__(self, **kwargs):
    super(Graph, self).__init__(**kwargs)
    self.date = None
    self.points = []
    self.touches = []
    self.dist = None
    self.variable = None
    self.zoom = 1.0
    self.offset = 0
    with self.canvas.before:
      Color(0,0,0)
      self.rect = Rectangle(pos=self.pos, size=self.size)
    self.bind(pos=self.update_rect, size=self.update_rect)
    
  def update_rect(self, *args):
    self.rect.pos = self.pos
    self.rect.size = self.size
    
  def set_var(self, variable):
    self.variable = variable
    self.calc_points()
    self.draw_points()
    
  def set_date(self, date):
    self.date = date
    self.calc_points()
    self.draw_points()
    
  def calc_points(self):
    if self.date is None or self.variable is None:
      return
    data = datastr.read(self.variable, self.date)
    del self.points[0:len(self.points)]
    min_val, max_val = self.variable.get_bounds()
    for item in data:
      scale_y = (int(item[2]) - min_val) / (max_val - min_val)
      y = self.height * scale_y + self.y
      str_time = util.get_time(item[3])
      scale_x = util.get_time_float(str_time)
      x = self.width * scale_x * self.zoom + self.x - self.offset * self.zoom
      self.points.append(x)
      self.points.append(y)
      
  def draw_points(self):
    self.canvas.clear()
    with self.canvas:
      Color(0.,0.,.5)
      Line(points=self.points)
    
  def set_zoom(self, zoom):
    if zoom < 1:
      self.zoom = 1
    elif zoom > 1440:
      self.zoom = 1440
    else: self.zoom = zoom
    self.calc_points()
    self.draw_points()
       
  def zoom_in(self, *args):
    self.set_zoom(self.zoom * 1.25)
    self.calc_points()
    self.draw_points()
    
  def zoom_out(self, *args):
    self.set_zoom(self.zoom * 0.8)
    self.calc_points()
    self.draw_points()
    
  def on_touch_down(self, touch):
    if not self.collide_point(touch.x, touch.y):
      return
    elif len(self.touches) < 2: 
      self.touches.append(touch)
    if len(self.touches) > 1:
      self.dist = self.touches[0].distance(self.touches[1])
    
  def on_touch_up(self, touch):
    del self.touches[0:len(self.touches)]
    self.dist = None
    
  def on_touch_move(self, touch):
    n_touches = len(self.touches)
    if n_touches == 1:
      min_offset = 0
      max_offset = self.width * self.zoom - self.width
      dx = touch.dx / self.zoom
      new_offset = self.offset + dx
      print self.offset, new_offset
      if new_offset < min_offset:
        self.offset = 0
      elif new_offset > max_offset:
        self.offset = max_offset
      else: self.offset = new_offset
      self.calc_points()
      self.draw_points()
    if n_touches > 1:
      curr_dist = self.touches[0].distance(self.touches[1])
      self.set_zoom(curr_dist / self.dist)