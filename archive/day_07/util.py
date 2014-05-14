import random, string, os


dirname = os.path.dirname(os.path.realpath(__file__))

def randomword(length):
   return ''.join(random.choice(string.uppercase) for i in range(length))