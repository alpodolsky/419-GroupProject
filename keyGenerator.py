import string
import random
def generateKey(cipher, stringLength = 9):
    if cipher == "PlayFair" or cipher == "Porta":
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
    elif cipher == "LaBoy":
        int1 = random.randint(0,100)
        int2 = random.randint(0,2500)
        return int1,int2

print(generateKey("LaBoy", 25))