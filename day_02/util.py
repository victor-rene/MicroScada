import random, string

def randomword(length):
   return ''.join(random.choice(string.uppercase) for i in range(length))