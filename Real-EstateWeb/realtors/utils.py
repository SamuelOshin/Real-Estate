import secrets
import string

def generate_random_password():
    letters = ''.join(secrets.choice(string.ascii_letters) for i in range(8))
    numbers = ''.join(secrets.choice(string.digits) for i in range(2))
    password = letters + numbers
    return password
