from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from datamgr import variables


class DataBindingEditor(FloatLayout):
  def __init__(self, widget, **kwargs):
    super(DataBindingEditor, self).__init__(**kwargs)
    dropdown = DropDown()
    
    for variable in variables:
      # when adding widgets, we need to specify the height manually (disabling
      # the size_hint_y) so the dropdown can calculate the area it needs.
      btn = Button(text='%s' % variable, size_hint_y=None, height=40)

      # for each button, attach a callback that will call the select() method
      # on the dropdown. We'll pass the text of the button as the data of the
      # selection.
      btn.bind(on_release=lambda btn: dropdown.select(btn.text))

      # then add the button inside the dropdown
      dropdown.add_widget(btn)

    # create a big main button
    mainbutton = Button(text=widget.variable.name, size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})

    # show the dropdown menu when the main button is released
    # note: all the bind() calls pass the instance of the caller (here, the
    # mainbutton instance) as the first argument of the callback (here,
    # dropdown.open.).
    mainbutton.bind(on_release=dropdown.open)

    # one last thing, listen for the selection in the dropdown list and
    # assign the data to the button text.
    dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
    dropdown.bind(on_select=lambda instance, x: widget.set_var(x))
    

    self.add_widget(mainbutton)
