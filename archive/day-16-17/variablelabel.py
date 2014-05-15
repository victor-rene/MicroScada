import os, util
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from datamgr import variables
# from variableeditor import VariableEditor
from variableselector import VariableSelector
from preferences import Preferences


class Binding:

  def __init__(self, source, source_attr, target, target_attr):
    self.source = source
    self.source_attr = source_attr
    self.target = target
    self.target_attr = target_attr
    
  def update(self, new_value):
    setattr(self.target, self.target_attr, str(new_value))
    # TODO check if str(new_value) is what I will always need


class VariableLabel(GridLayout):

  def __init__(self, **kwargs):
    super(VariableLabel, self).__init__(**kwargs)
    self.cols = 4
    self.rows = 1
    self.variable = None
    self.listeners = []
    with self.canvas:
      if Preferences.theme != 'default':
        src = os.path.join(util.dir_theme, Preferences.theme, 'label.png')
        self.background = Image(source=src, pos=self.pos, size=self.size,
            allow_stretch=True, keep_ratio=False)
      else:
        Color(.1,.1,.1)
        self.background = Rectangle(pos=self.pos, size=self.size)
      self.bind(pos=self.update_bg)
      self.bind(size=self.update_bg)
    lbl_tip = Label(text='Click to choose variable', color = Preferences.foreground)
    self.add_widget(lbl_tip)
    
  def set_var(self, name):
    self.clear_widgets()
    variable = variables[name]
    self.variable = variable
    lbl_name = Label(text=variable.name, color = Preferences.foreground)
    lbl_text = Label(text=variable.text, color = Preferences.foreground)
    lbl_value = Label(text=str(variable.value), color = Preferences.foreground)
    self.add_widget(lbl_name)
    self.add_widget(lbl_text)
    self.add_widget(lbl_value)
    if 'unit' in variable.meta:
      lbl_unit = Label(text=variable.meta['unit'], size_hint=[.5, 0], color = Preferences.foreground)
      self.add_widget(lbl_unit)
    b_text = Binding(variable, 'text', lbl_text, 'text')
    b_value = Binding(variable, 'value', lbl_value, 'text')
    variable.bindings.append(b_text)
    variable.bindings.append(b_value)
    for listener in self.listeners:
      listener.set_var(variable)
      
  def update_bg(self, *args):
    self.background.pos = self.pos
    self.background.size = self.size
    
  def on_touch_down(self, touch):
    if not self.collide_point(touch.x, touch.y):
      return
    popup = Popup(title='Edit variable',
      content=VariableSelector(self),
      size_hint=(None, None), size=(400, 400))
    popup.open()
    
  def append_listener(self, widget):
    self.listeners.append(widget)
    
  def remove_listener(self, widget):
    self.listeners.remove(widget)