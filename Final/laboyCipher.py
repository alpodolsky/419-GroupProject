from random import random, randint
def encrypt(message, key1, key2):
    hold = ''
    encrypted= []
    # key1 = randint(0,10000)
    # print("Key 1: ",key1)

    for i in range(len(message)):
        char = message[i]
        if char == " " or char == '.':
            hold = hold + char
            continue
        if char.isupper():
            hold += chr((ord(char) + key1 -65) % 26 +65)
            continue
        else:
            hold += chr((ord(char) + key1-97) % 26 + 97)
    print("caesar cipher: " + hold)
    # key2 = randint(0,50)
    # print("Key 2: " ,key2)
    for i in hold:
        x = ord(i) - key2
        encrypted.append(x)
    print("Encrypted message: ")
    for i in encrypted:
        print(i, end='')

    print()
    return encrypted
    # decrypt(message, encrypted, key1, key2)

def decrypt(encrypted, key1, key2):
    decrypted = ""
    for i in encrypted:
        x = int(i)
        x = x + key2
        x = chr(x)
        decrypted += x
    print("Reverted casear:" ,decrypted)
    hold = ''
    for i in range(len(decrypted)):
        char = decrypted[i]
        if char == " " or char == '.':
            hold += char
            continue
        if char.isupper():
            hold += chr((ord(char) - key1 -65) % 26 + 65)
            continue
        else:
            hold += chr((ord(char) - key1 -97) % 26 + 97)
    decrypted = hold
    # if decrypted != message:
    #     decrypted = message
    # print("Decrpyted message:", decrypted)

    return decrypted

def main():

    message = input("Input message: ")
    encrypted_message = encrypt(message, 24, 100)
    print(encrypted_message)
    print(decrypt(encrypted_message, 24, 100))

if __name__ == '__main__':
    main()