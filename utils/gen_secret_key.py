import os


# openssl rand -hex 32
def generate_secret_key():
    return os.urandom(32).hex()


if __name__ == "__main__":
    SECRET_KEY = generate_secret_key()
    print(SECRET_KEY)
