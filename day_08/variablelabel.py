from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from datamgr import variables


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
    with self.canvas:
      Color(.1,.1,.1)
      self.rect = Rectangle(pos=self.pos, size=self.size)
      self.bind(pos=self.update_rect)
      self.bind(size=self.update_rect)
    
  def set_var(self, name):
    variable = variables[name]
    self.variable = variable
    lbl_name = Label(text=variable.name)
    lbl_text = Label(text=variable.text)
    lbl_value = Label(text=str(variable.value))
    self.add_widget(lbl_name)
    self.add_widget(lbl_text)
    self.add_widget(lbl_value)
    if 'unit' in variable.meta:
      lbl_unit = Label(text=variable.meta['unit'], size_hint=[.5, 0])
      self.add_widget(lbl_unit)
    b_text = Binding(variable, 'text', lbl_text, 'text')
    b_value = Binding(variable, 'value', lbl_value, 'text')
    variable.bindings.append(b_text)
    variable.bindings.append(b_value)
    
  def update_rect(self, *args):
    self.rect.pos = self.pos
    self.rect.size = self.size
