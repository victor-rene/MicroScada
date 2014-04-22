import os
from variable import Variable
from datasource import DataSource
from datastore import DataStore

variables = dict()

variables['pressure'] = Variable('MW_01', 'word', 'Pressure')
variables['temperature'] = Variable('MW_02', 'dword', 'Temperature')
variables['warning'] = Variable('M_01', 'bool', 'Warning')

datasrc = DataSource('offline')
datastr = DataStore()

dirname = os.path.dirname(os.path.realpath(__file__))
datastr.connect(os.path.join(dirname, 'microscada.s3db'))

def scan(dt):
  for variable in variables.itervalues():
    val = datasrc.read(variable)
    variable.set_value(val)
    datastr.write(variable)
