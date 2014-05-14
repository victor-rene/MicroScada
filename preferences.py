from random import randint
from kivy.graphics import Color


class Preferences:
  theme = None
  foreground = None
  background = None
    
  @classmethod
  def light_theme(cls, *args):
    cls.theme = 'light'
    cls.foreground = [.1,.1,.1,1]
    cls.background = [.9,.9,.9,1]
    
  @classmethod
  def dark_theme(cls, *args):
    cls.theme = 'dark'
    cls.foreground = [.9,.9,.9,1]
    cls.background = [.1,.1,.1,1]
    
  @classmethod
  def default_theme(cls, *args):
    cls.theme = 'default'
    cls.foreground = [1,1,1,1]
    cls.background = [0,0,0,1]
    
  @classmethod
  def random_theme(cls):
    i = randint(0, 1)
    if i == 0: cls.light_theme()
    else: cls.dark_theme()
    

Preferences.random_theme()