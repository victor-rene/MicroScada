import os
from variable import Variable
from datasource import DataSource
from datastore import DataStore
from kivy.clock import Clock


variables = dict()

variables['MW_01'] = Variable('MW_01', 'word', 'Pressure')
variables['MW_02'] = Variable('MW_02', 'dword', 'Temperature')
variables['M_01'] = Variable('M_01', 'bool', 'Warning')

datasrc = DataSource('offline')
datastr = DataStore()

dirname = os.path.dirname(os.path.realpath(__file__))
datastr.connect(os.path.join(dirname, 'microscada.s3db'))

scheduling = None

def scan(dt):
  for variable in variables.itervalues():
    val = datasrc.read(variable)
    variable.set_value(val)
    datastr.write(variable)
  print scheduling
  return scheduling

    
def start_clock(a):
  print a
  Clock.schedule_interval(scan, 1.0)
  scheduling = True
  
  
def stop_clock(a):
  print a
  scheduling = False