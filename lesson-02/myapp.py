import random
import string
import time
SPEC_SYMBOLS = "#.,!@&^%*"


def generate_password_string() -> str:
    length: int = random.randint(8, 16)
    alphabet: str = string.ascii_lowercase + string.ascii_uppercase + string.digits + SPEC_SYMBOLS
    password: str = ''.join(random.choice(alphabet) for _ in range(length))
    return password

def is_correct_password(password: str) -> bool:
    checks = [
        lambda p: any(c.isdigit() for c in p),
        lambda p: any(c.islower() for c in p),
        lambda p: any(c.isupper() for c in p),
        lambda p: any(c in SPEC_SYMBOLS for c in p)
    ]
    return all([check(password) for check in checks])

def generate_password() -> str:
    password: str = generate_password_string()

    while not is_correct_password(password):
        password = generate_password_string()

    time.sleep(0.05) # thinking...
    return password


def app(environ, start_response):
    password = generate_password()
    data = f"Your password: {password}\n".encode()
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return iter([data])
