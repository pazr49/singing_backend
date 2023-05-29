import random
import string

def generate_random_string(prefix):
    characters = string.ascii_letters + string.digits  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    random_string = ''.join(random.choice(characters) for _ in range(20))
    return prefix + "_" + random_string

# Generate a random string
random_string = generate_random_string(prefix="part")
print(random_string)
