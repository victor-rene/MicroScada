import util
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.label import Label
from datamgr import datastr, variables, load_vars
from preferences import Preferences


class GraphLabel(Label):

  def __init__(self, **kwargs):
    super(GraphLabel, self).__init__(**kwargs)
    self.color = Preferences.foreground
    
  def set_var(self, variable):
    bounds = variable.get_bounds()
    if 'min' in self.id:
      self.text = str(bounds[0])
    elif 'max' in self.id:
      self.text = str(bounds[1])
    

class Graph(FloatLayout):

  def __init__(self, **kwargs):
    super(Graph, self).__init__(**kwargs)
    self.date = util.get_date_now()
    self.points = []
    self.touches = []
    self.dist = None
    self.variable = None
    self.zoom = 1.0
    self.offset = 0
    self.listeners = []
    load_vars()
    with self.canvas.before:
      Color(.1,.1,.1)
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
      scale_y = (float(item[2]) - min_val) / float(max_val - min_val)
      y = self.height * scale_y + self.y
      str_time = util.get_time(item[3])
      scale_x = util.get_time_float(str_time)
      x = self.width * scale_x * self.zoom + self.x - self.offset
      if x >= self.x and x <= self.right:
        self.points.append(x)
        self.points.append(y)
      
  def draw_points(self):
    self.canvas.clear()
    with self.canvas.before:
      Color(.5,.5,.5)
      mid_y = self.y + self.height / 2
      mid_y_25 = self.y + self.height / 4
      mid_y_75 = self.y + self.height * 3 / 4
      Line(points = [self.x, mid_y, self.right, mid_y])
      Line(points = [self.x, mid_y_25, self.right, mid_y_25])
      Line(points = [self.x, mid_y_75, self.right, mid_y_75])
    with self.canvas:
      Color(0.,0.,.5)
      Line(points=self.points)
    with self.canvas.after:
      Color(1,1,1)
      mid_x = self.x + self.width / 2
      Line(points = [mid_x, self.y, mid_x, self.top])

  def set_zoom(self, zoom):
    if zoom < 1:
      self.zoom = 1
    elif zoom > 1440:
      self.zoom = 1440
    else: self.zoom = zoom
    self.calc_points()
    self.draw_points()
       
  def zoom_in(self, *args):
    self.set_zoom(self.zoom * 2)
    self.offset = self.offset * 2 + self.width / 2
    self.calc_points()
    self.draw_points()
    from pageloader import get_widget
    get_widget('lbl_zoom').text = 'x' + str(self.zoom)
    
  def zoom_out(self, *args):
    self.set_zoom(self.zoom * .5)
    self.offset = (self.offset - self.width / 2 ) * .5 
    self.calc_points()
    self.draw_points()
    from pageloader import get_widget
    get_widget('lbl_zoom').text = 'x' + str(self.zoom)
    
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
      # print self.offset, new_offset
      if new_offset < min_offset:
        self.offset = 0
      elif new_offset > max_offset:
        self.offset = max_offset
      else: self.offset = new_offset
      self.calc_points()
      self.draw_points()
      self.set_times()
    if n_touches > 1:
      curr_dist = self.touches[0].distance(self.touches[1])
      self.set_zoom(curr_dist / self.dist)
    
  def append_listener(self, widget):
    self.listeners.append(widget)
    
  def remove_listener(self, widget):
    self.listeners.remove(widget)
    
  def set_times(self):
    t_mid = (self.offset + self.width / 2) / (self.zoom * self.width)
    str_mid = util.get_time_str(t_mid)
    t_min = self.offset / (self.zoom * self.width)
    str_min = util.get_time_str(t_min)
    t_max = (self.offset + self.width) / (self.zoom * self.width)
    str_max = util.get_time_str(t_max)
    for listener in self.listeners:
      if 'max' in listener.id:
        listener.text = str_max
      elif 'mid' in listener.id:
        listener.text = str_mid
      elif 'min' in listener.id:
        listener.text = str_min