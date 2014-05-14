import random, string, os, datetime


dir_root = os.path.dirname(os.path.realpath(__file__))
dir_theme = os.path.join(dir_root, 'theme')
dir_img = os.path.join(dir_root, 'img')

def randomword(length):
   return ''.join(random.choice(string.uppercase) for i in range(length))
   
def get_time_float(s):
  h = int(s[0:2])
  m = int(s[3:5])
  s = int(s[6:8])
  return h / 24.0 + m / (24.0 * 60.0) + s / (24.0 * 60.0 * 60)
  
def get_time(s):
  return s.split()[1]
  
def get_date_now():
  now = datetime.datetime.now()
  year = str(now.year)
  month = str(now.month).zfill(2)
  day = str(now.day).zfill(2)
  return year + '-' + month + '-' + day