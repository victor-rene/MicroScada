from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput


class VariableEditor(FloatLayout):
  def __init__(self, variable, **kwargs):
    super(VariableEditor, self).__init__(**kwargs)
    self.variable = variable
    lbl_name = Label(text='Name', pos_hint={'center_x': 0.2, 'center_y': 0.9})
    lbl_type = Label(text='Type', pos_hint={'center_x': 0.2, 'center_y': 0.8})
    lbl_text = Label(text='Text', pos_hint={'center_x': 0.2, 'center_y': 0.7})
    ti_name = TextInput(text=variable.name, multiline=False, pos_hint={'center_x': 0.8, 'center_y': 0.9}, size_hint=(0.3, .1))
    ti_type = TextInput(text=variable.type, multiline=False, pos_hint={'center_x': 0.8, 'center_y': 0.8}, size_hint=(0.3, .1))
    ti_text = TextInput(text=variable.text, multiline=False, pos_hint={'center_x': 0.8, 'center_y': 0.7}, size_hint=(0.3, .1))
    self.add_widget(lbl_name)
    self.add_widget(lbl_type)
    self.add_widget(lbl_text)
    self.add_widget(ti_name)
    self.add_widget(ti_type)
    self.add_widget(ti_text)
    #self.bindings = []
    #self.meta = dict()