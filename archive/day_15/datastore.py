import sqlite3
import datetime


class DataStore:

  def __init__(self):
    self.conn = None
    
  def read(self, variable, date):
    """
    Date format: YYYY-MM-DD.
    """
    if self.is_connected():
      c = self.conn.cursor()
      q = 'SELECT * FROM curve WHERE name="' + variable.name + '" AND time LIKE "' + date + '%" ORDER BY time ASC'
      c.execute(q)
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