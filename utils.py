import random
import string
from werkzeug.security import generate_password_hash, check_password_hash

def generate_random_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def check_password_hash(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)
