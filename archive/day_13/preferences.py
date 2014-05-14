class Preferences:
  theme = 'default'
  color = [1,1,1,1]
    
  @classmethod
  def light_theme(cls, touch):
    cls.theme = 'light'
    cls.color = [0,0,0,1]
    
  @classmethod
  def dark_theme(cls, touch):
    cls.theme = 'dark'
    cls.color = [1,1,1,1]
    
  @classmethod
  def default_theme(cls, touch):
    cls.theme = 'default'
    cls.color = [1,1,1,1]