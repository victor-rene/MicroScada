from kivy.graphics import Color


class Preferences:
  theme = 'default'
  foreground = [1,1,1,1]
  background = [0,0,0,1]
    
  @classmethod
  def light_theme(cls, touch):
    cls.theme = 'light'
    cls.foreground = [0,0,0,1]
    cls.background = [1,1,1,1]
    
  @classmethod
  def dark_theme(cls, touch):
    cls.theme = 'dark'
    cls.foreground = [1,1,1,1]
    cls.background = [0,0,0,1]
    
  @classmethod
  def default_theme(cls, touch):
    cls.theme = 'default'
    cls.foreground = [1,1,1,1]
    cls.background = [0,0,0,1]
