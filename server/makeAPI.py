import random

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

API_KEY = ''

for _ in range(20):

    API_KEY = API_KEY + random.choice(chars)

print(API_KEY)
print(API_KEY)
