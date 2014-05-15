#!/usr/local/bin/python
# coding: utf-8

import os
from util import dir_root
from variable import Variable
from datasource import DataSource
from datastore import DataStore
from kivy.clock import Clock


variables = dict()

variables['PRESS'] = Variable('PRESS', 'word', 'Pressure')
variables['PRESS'].meta['unit'] = 'mbar'
variables['TEMP'] = Variable('TEMP', 'dword', 'Temperature')
variables['TEMP'].meta['unit'] = '°C'
variables['WARN'] = Variable('WARN', 'bool', 'Warning')

datasrc = DataSource('offline')
datastr = DataStore()
datastr.connect(os.path.join(dir_root, 'data', 'microscada.s3db'))

def load_vars():
  names = datastr.get_var_names()
  for name in names:
    if 'GAUGE' in name:
      variable = Variable(name, 'word', 'Gauge')
      variable.meta['min'] = 0
      variable.meta['max'] = 20
      variables[name] = variable


class Scheduler:
  running = False

  @staticmethod
  def process(dt):
    for variable in variables.itervalues():
      if 'GAUGE' in variable.name:
        continue # interaction bug between the variables above and the others
      val = datasrc.read(variable)
      variable.set_value(val)
      datastr.write(variable)
    return Scheduler.running

  @staticmethod    
  def start(instance):
    Clock.schedule_interval(Scheduler.process, 1.0)
    Scheduler.running = True
    
  @staticmethod  
  def stop(instance):
    Scheduler.running = False