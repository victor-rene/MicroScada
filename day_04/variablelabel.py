from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
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
    self.cols = 3
    self.rows = 1
    self.variable = None
    
  def set_var(self, name):
    variable = variables[name]
    self.variable = variable
    lbl_name = Label(text=variable.name)
    lbl_text = Label(text=variable.text)
    lbl_value = Label(text=str(variable.value))
    self.add_widget(lbl_name)
    self.add_widget(lbl_text)
    self.add_widget(lbl_value)
    b_text = Binding(variable, 'text', lbl_text, 'text')
    b_value = Binding(variable, 'value', lbl_value, 'text')
    variable.bindings.append(b_text)
    variable.bindings.append(b_value)
