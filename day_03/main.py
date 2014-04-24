from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.clock import Clock
from datamgr import variables, scan


class Binding:

  def __init__(self, source, source_attr, target, target_attr):
    self.source = source
    self.source_attr = source_attr
    self.target = target
    self.target_attr = target_attr
    
  def update(self, new_value):
    setattr(self.target, self.target_attr, str(new_value))
    # TODO check if str(new_value) is what I will always need

    
class RootWidget(BoxLayout):

  def __init__(self, **kwargs):
    super(RootWidget, self).__init__(**kwargs)
    for variable in variables.itervalues():
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

     
class MyApp(App):
  def build(self):
    rw = RootWidget()
    Clock.schedule_interval(scan, 1.0)
    return rw


if __name__ == '__main__':
   MyApp().run()