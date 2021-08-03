import string
import secrets
alphabet = string.hexdigits + '~!@#$%^&*'
while True:
    password = ''.join(secrets.choice(alphabet) for i in range(16))
    if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3):
        break
print(password)
