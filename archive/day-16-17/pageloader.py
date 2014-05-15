import os, util
import yaml
import datamgr
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Callback, Color
from variablelabel import VariableLabel
from thermometer import Thermometer
from manometer import Manometer
from led import Led
from editor import Editor, EditGrid
from simulator import Simulator, SimulGrid
from themebutton import ThemeButton
from preferences import Preferences
from graph import Graph, GraphLabel
from datepicker import DatePicker


class RootWidget(FloatLayout):

  def __init__(self, **kwargs):
    super(RootWidget, self).__init__(**kwargs)
    self.bind(pos=self.draw_rect, size=self.draw_rect)

  def draw_rect(self, *args):
    with self.canvas.before:
      Color(Preferences.background[0], Preferences.background[1], Preferences.background[2], 1)
      Rectangle(pos=self.pos, size=self.size)

        
root_widget = RootWidget()
links = dict()


def load_page(name):
  filename = os.path.join(util.dir_root, 'page', name + '.yaml')
  stream = file(filename, 'r')
  return yaml.load(stream)
  
  
def build_page(layout, page):
  layout.clear_widgets()
  links.clear() # TODO: will prevent iframe functionality to work
  for id, item in page.iteritems(): # create instances (ids)
    if item['type'] == 'button':
      wgt = Button()
      if Preferences.theme != 'default':
        wgt.background_normal = os.path.join(util.dir_theme, Preferences.theme, 'btn_normal.png')
        wgt.background_down = os.path.join(util.dir_theme, Preferences.theme, 'btn_down.png')
        wgt.color = Preferences.foreground
        wgt.border = [0,0,0,0]
    elif item['type'] == 'label':
      wgt = Label()
      if Preferences.theme != 'default':
        wgt.color = Preferences.foreground
    elif item['type'] == 'image':
      img_path = os.path.join(util.dir_img, item['source'])
      wgt = Image(source=img_path)
    elif item['type'] == 'textinput':
      wgt = TextInput()
    elif item['type'] == 'var-label':
      wgt = VariableLabel()
    elif item['type'] == 'led':
      wgt = Led()
    elif item['type'] == 'thermometer':
      wgt = Thermometer()
    elif item['type'] == 'manometer':
      wgt = Manometer()
    elif item['type'] == 'edit-grid':
      wgt = EditGrid()
      wgt.set_dimenstion(item['rows'], item['cols'])
    elif item['type'] == 'simul-grid':
      wgt = SimulGrid()
      wgt.set_dimenstion(item['rows'], item['cols'])
      wgt.build_network()
      Simulator.set_grid(wgt)
    elif item['type'] == 'graph':
      wgt = Graph()
    elif item['type'] == 'DatePicker':
      wgt = DatePicker()
    elif item['type'] == 'GraphLabel':
      wgt = GraphLabel()
    else:
      print 'Unknown component ' + item['type']
      return
    wgt.id = id
    layout.add_widget(wgt)
  for id, item in page.iteritems(): # now can use references (id)
    wgt = get_widget(id)
    if 'text' in item:
      wgt.text = item['text']
    if 'font_size' in item:
      wgt.font_size = item['font_size']
    if 'pos' in item:
      wgt.pos = eval(item['pos'])
    if 'size' in item:
      wgt.size = eval(item['size'])
    if 'pos_hint' in item:
      wgt.pos_hint = item['pos_hint']
    if 'size_hint' in item:
      wgt.size_hint = eval(item['size_hint'])
    if 'link' in item:
      links[wgt.id] = item['link']
      wgt.bind(on_press=navigate)
    if 'click' in item:
      wgt.bind(on_press=eval(item['click']))
    if 'halign' in item:
      wgt.halign = item['halign']
    if 'multiline' in item:
      wgt.multiline = item['multiline']
    if 'validate' in item:
      wgt.bind(on_text_validate=eval(item['validate']))
    if 'variable' in item:
      wgt.set_var(item['variable'])
    if 'listener' in item:
      listeners = item['listener'].split(',')
      for listener in listeners:
        wgt.append_listener(get_widget(listener.strip()))
    if 'markup' in item:
      wgt.markup = item['markup']
    
  
  
def open_page(name, layout=None):
  page = load_page(name)
  if layout is None:
    root_widget.draw_rect()
    build_page(root_widget, page)
  else: build_page(layout, page)
  
  
def navigate(instance):
  target = links[instance.id]
  open_page(target)
  
  
def get_widget(id):
  for wgt in root_widget.children:
    print wgt.id
    if wgt.id == id:
      return wgt
    
  