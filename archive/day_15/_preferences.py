class Preferences:
  root_widget = None

  @staticmethod
  def set_width(instance):
    width = int(instance.text)
    height = Preferences.root_widget.height
    Preferences.root_widget.size = [width, height]
    
  @staticmethod
  def set_height(instance):
    width = Preferences.root_widget.width
    height = int(instance.text)
    Preferences.root_widget.size = [width, height]
   
  @staticmethod
  def set_root_widget(wgt):
    Preferences.root_widget = wgt