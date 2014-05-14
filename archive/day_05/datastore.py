import sqlite3
import datetime


class DataStore:

  def __init__(self):
    self.conn = None
    
  def read(variable):
    if self.is_connected():
      c = self.conn.cursor()
      t = (variable.name,)
      c.execute('SELECT * FROM curve WHERE name=? ORDER BY time ASC', t)
      return c.fetchall()
    else:
      print 'Not connected'
      return None
    
  def write(self, variable):
    if self.conn != None:
      c = self.conn.cursor()
      t = (variable.name, str(variable.value), str(datetime.datetime.now()))
      print str(t)
      c.execute('INSERT INTO curve(name, value, time) VALUES ' + str(t))
      self.conn.commit()
    else:
      print 'Not connected'
    
  def connect(self, connstr):
    if not self.is_connected():
      self.conn = sqlite3.connect(connstr)
      print 'Connection opened'
    else: print 'Already connected'
    
  def disconnect(self):
    self.conn.close()
    self.conn = None
    print 'Connection closed'
    
  def is_connected(self):
    return self.conn != None