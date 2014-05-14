import os
import yaml
import datamgr
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from variablelabel import VariableLabel
from thermometer import Thermometer
from manometer import Manometer
from led import Led
from editor import Editor, EditGrid
from simulator import Simulator, SimulGrid
from themebutton import ThemeButton
from preferences import Preferences


root_widget = FloatLayout()
links = dict()


def load_page(name):
  curr_dir = os.path.dirname(os.path.realpath(__file__))
  filename = os.path.join(curr_dir, 'page', name + '.yaml')
  stream = file(filename, 'r')
  return yaml.load(stream)
  
  
def build_page(layout, page):
  layout.clear_widgets()
  links.clear() # TODO: will prevent iframe functionality to work
  for id, item in page.iteritems():
    if item['type'] == 'button':
      wgt = Button()
    elif item['type'] == 'theme-button':
      wgt = ThemeButton(Preferences.theme)
    elif item['type'] == 'label':
      wgt = Label()
    elif item['type'] == 'textinput':
      wgt = TextInput()
    elif item['type'] == 'var-label':
      wgt = VariableLabel()
      wgt.set_var(item['variable'])
    elif item['type'] == 'led':
      wgt = Led()
      wgt.set_var(item['variable'])
    elif item['type'] == 'thermometer':
      wgt = Thermometer()
      wgt.set_var(item['variable'])
    elif item['type'] == 'manometer':
      wgt = Manometer()
      wgt.set_var(item['variable'])
    elif item['type'] == 'edit-grid':
      wgt = EditGrid()
      wgt.set_dimenstion(item['rows'], item['cols'])
    elif item['type'] == 'simul-grid':
      wgt = SimulGrid()
      wgt.set_dimenstion(item['rows'], item['cols'])
      wgt.build_network()
      Simulator.set_grid(wgt)
    else:
      print 'Unknown component ' + item['type']
      return
    wgt.id = id
    if 'text' in item:
      print repr(item['text'])
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
    layout.add_widget(wgt)
  
  
def open_page(name, layout=None):
  page = load_page(name)
  if layout is None:
    build_page(root_widget, page)
  else: build_page(layout, page)
  
  
def navigate(instance):
  target = links[instance.id]
  open_page(target)
  