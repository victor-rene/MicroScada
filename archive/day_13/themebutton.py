import os, util
from kivy.uix.button import Button
from preferences import Preferences


class ThemeButton(Button):

  def __init__(self, theme, **kwargs):
    super(ThemeButton, self).__init__(**kwargs)
    if theme != 'default':
      self.background_normal = os.path.join(util.dir_theme, 'btn_' + theme + '_up.png')
      self.background_down = os.path.join(util.dir_theme, 'btn_' + theme + '_down.png')
      self.color = Preferences.color