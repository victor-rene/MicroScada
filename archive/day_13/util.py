import random, string, os


dir_root = os.path.dirname(os.path.realpath(__file__))
dir_theme = os.path.join(dir_root, 'theme')
dir_img = os.path.join(dir_root, 'img')

def randomword(length):
   return ''.join(random.choice(string.uppercase) for i in range(length))