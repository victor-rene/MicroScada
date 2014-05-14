import os, util, datetime
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty
from preferences import Preferences


class DatePicker(GridLayout):
  year = NumericProperty(datetime.datetime.now().year)
  month = NumericProperty(datetime.datetime.now().month)
  day = NumericProperty(datetime.datetime.now().day)

  def __init__(self, **kwargs):
    super(DatePicker, self).__init__(**kwargs)
    self.cols = 3
    self.rows = 3
    self.btn_up_year = self.styled_button('up')
    self.btn_up_month = self.styled_button('up')
    self.btn_up_day = self.styled_button('up')
    self.lbl_year = Label()
    self.lbl_month = Label()
    self.lbl_day = Label()
    self.lbl_year.color = Preferences.foreground
    self.lbl_month.color = Preferences.foreground
    self.lbl_day.color = Preferences.foreground
    self.btn_down_year = self.styled_button('down')
    self.btn_down_month = self.styled_button('down')
    self.btn_down_day = self.styled_button('down')
    self.btn_up_year.bind(on_press=self.inc_year)
    self.btn_up_month.bind(on_press=self.inc_month)
    self.btn_up_day.bind(on_press=self.inc_day)
    self.btn_down_year.bind(on_press=self.dec_year)
    self.btn_down_month.bind(on_press=self.dec_month)
    self.btn_down_day.bind(on_press=self.dec_day)
    self.add_widget(self.btn_up_year)
    self.add_widget(self.btn_up_month)
    self.add_widget(self.btn_up_day)
    self.add_widget(self.lbl_year)
    self.add_widget(self.lbl_month)
    self.add_widget(self.lbl_day)
    self.add_widget(self.btn_down_year)
    self.add_widget(self.btn_down_month)
    self.add_widget(self.btn_down_day)
    self.bind(year=self.update_date)
    self.bind(month=self.update_date)
    self.bind(day=self.update_date)
    self.listeners = []
    self.update_date()
    
  def update_date(self, *args):
    list_date = [str(self.year), str(self.month).zfill(2), str(self.day).zfill(2)]
    self.lbl_year.text = list_date[0]
    self.lbl_month.text = list_date[1]
    self.lbl_day.text = list_date[2]
    date = list_date[0] + "-" + list_date[1] + "-" + list_date[2]
    for listener in self.listeners:
      listener.set_date(date)
    
  def inc_year(self, *args):
    self.year += 1
    
  def dec_year(self, *args):
    self.year -= 1
    
  def inc_month(self, *args):
    if self.month == 12:
      self.month = 1
    else: self.month += 1
    
  def dec_month(self, *args):
    if self.month == 1:
      self.month = 12
    else: self.month -= 1
    
  def inc_day(self, *args):
    if self.day == 31:
      self.day = 1
    else: self.day += 1
    
  def dec_day(self, *args):
    if self.day == 1:
      self.day = 31
    else: self.day -= 1
    
  def append_listener(self, widget):
    self.listeners.append(widget)
    
  def remove_listener(self, widget):
    self.listeners.remove(widget)
    
  def styled_button(self, orientation):
    btn = Button()
    if orientation == 'up':
      btn.background_normal = os.path.join(util.dir_img, 'datepicker_00.png')
      btn.background_down = os.path.join(util.dir_img, 'datepicker_01.png')
      btn.border = [0,0,0,0]
    elif orientation == 'down':
      btn.background_normal = os.path.join(util.dir_img, 'datepicker_10.png')
      btn.background_down = os.path.join(util.dir_img, 'datepicker_11.png')
      btn.border = [0,0,0,0]
    return btn