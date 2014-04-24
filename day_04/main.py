from kivy.app import App
from kivy.clock import Clock
from datamgr import variables, scan
from pageloader import root_widget, open_page




    # for variable in variables.itervalues():
      # lbl_name = Label(text=variable.name)
      # lbl_text = Label(text=variable.text)
      # lbl_value = Label(text=str(variable.value))
      # self.add_widget(lbl_name)
      # self.add_widget(lbl_text)
      # self.add_widget(lbl_value)
      # b_text = Binding(variable, 'text', lbl_text, 'text')
      # b_value = Binding(variable, 'value', lbl_value, 'text')
      # variable.bindings.append(b_text)
      # variable.bindings.append(b_value)

  
  
class MyApp(App):
  def build(self):
    open_page('home')
    #Clock.schedule_interval(scan, 1.0)
    return root_widget


if __name__ == '__main__':
   MyApp().run()