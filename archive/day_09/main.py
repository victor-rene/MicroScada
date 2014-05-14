from kivy.app import App
from kivy.clock import Clock
from datamgr import variables
from pageloader import root_widget, open_page

  
class MyApp(App):
  def build(self):
    open_page('home')
    return root_widget


if __name__ == '__main__':
   MyApp().run()