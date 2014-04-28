#!/usr/local/bin/python
# coding: utf-8

import os
from util import dirname
from variable import Variable
from datasource import DataSource
from datastore import DataStore
from kivy.clock import Clock


variables = dict()

variables['MW_01'] = Variable('MW_01', 'word', 'Pressure')
variables['MW_01'].meta['unit'] = 'mbar'
variables['MW_02'] = Variable('MW_02', 'dword', 'Temperature')
variables['MW_02'].meta['unit'] = '°C'
variables['M_01'] = Variable('M_01', 'bool', 'Warning')

datasrc = DataSource('offline')
datastr = DataStore()
datastr.connect(os.path.join(dirname, 'microscada.s3db'))


class Scheduler:
  running = False

  @staticmethod
  def process(dt):
    for variable in variables.itervalues():
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