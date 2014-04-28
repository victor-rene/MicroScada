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


class Scheduler:
  running = False

  @staticmethod
  def process(dt):
    for variable in variables.itervalues():
      val = datasrc.read(variable)
      variable.set_value(val)
      datastr.write(variable)
    print Scheduler.running
    return Scheduler.running

  @staticmethod    
  def start(instance):
    Clock.schedule_interval(Scheduler.process, 1.0)
    Scheduler.running = True
    
  @staticmethod  
  def stop(instance):
    Scheduler.running = False