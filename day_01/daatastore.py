import sqlite3


class DataStore:
  def __init__(self):
    self.conn = None
    
  def read(name):
    if self.conn != None:
      c = self.conn.cursor()
      t = (name,)
      c.execute('SELECT * FROM datapoints WHERE name=? ORDER BY time ASC', t)
      return c.fetchall()
    else:
      print 'Not connected'
      return None
    
  def write(name):
    if self.conn != None:
      c = self.conn.cursor()
      t = (name, value, time)
      c.execute('INSERT INTO datapoints VALUES ?', t)
      self.conn.commit()
    else:
      print 'Not connected'
    
  def connect(self, connstr):
    self.conn = sqlite3.connect(connstr)
    
  def disconnect(self):
    self.conn.close()