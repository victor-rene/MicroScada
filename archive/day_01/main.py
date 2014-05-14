from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty


class RootWidget(BoxLayout):

  def __init__(self, **kwargs):
    super(RootWidget, self).__init__(**kwargs)
    self.add_widget(Label(text='Pressure'))

  def update(self):
    for child in self.children:
      child.update()

     
class CustomBtn(Widget):

  pressed = ListProperty([0, 0])

  def on_touch_down(self, touch):
     if self.collide_point(*touch.pos):
         self.pressed = touch.pos
         # we consumed the touch. return False here to propagate
         # the touch further to the children.
         return True
     return super(CustomBtn, self).on_touch_down(touch)

  def on_pressed(self, instance, pos):
     print ('pressed at {pos}'.format(pos=pos))

Clock.schedule_interval(update, 1 / 60.)
     
class LabelValue(Widget):
  text = StringProperty(None)
  value = NumericProperty(None)

  def update(self):
    self.text = 
    self.value = variables[]  
  
  def on_touch_down(self, touch):
    if self.collide_point(*touch.pos):
      self.pressed = touch.pos
      # we consumed the touch. return False here to propagate
      # the touch further to the children.
      return True
    return super(LebeledValue, self).on_touch_down(touch)

  def on_pressed(self, instance, pos):
    print ('pressed at {pos}'.format(pos=pos))
     
class MyApp(App):
  def build(self):
    rw = RootWidget()
    Clock.schedule_interval(rw.update, 1.0 / 60.0)
    return rw


if __name__ == '__main__':
   TestApp().run()