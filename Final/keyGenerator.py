import string
import random
def generateKey(cipher, stringLength = 9):
    if cipher == "playfair" or cipher == "porta":
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
    elif cipher == "laboy":
        int1 = random.randint(0,100)
        int2 = random.randint(0,2500)
        return (int1,int2)