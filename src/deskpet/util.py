import random

def RandomID(n=8,s="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"):
    return "".join(random.choice(s) for _ in range(n))
