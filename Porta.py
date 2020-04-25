import numpy as np

def create_table():
    firsthalf = 'abcdefghijklm'
    secondhalf = 'nopqrstuvwxyz'

    matrix = np.chararray((13, 26))

    index = 0
    index4 = 0

    for i in range(len(firsthalf)):
        index2 = index
        for j in range(len(secondhalf)):
            letter = secondhalf[index2]
            matrix[i][j] = letter

            if index2 + 1 == 13:
                index2 = 0
            else:
                index2+=1
        
        index3 = index4
        for j in range(len(secondhalf)):
            letter = firsthalf[index3]
            matrix[i][j+13] = letter

            if index3 + 1 == 13:
                index3 = 0
            else:
                index3+=1
        
        if index+1 == 13:
            index = 0
        else:
            index+=1
        if index4 == 0:
            index4 = 12
        else:
            index4 -= 1
    
    return matrix

def encrypt(plaintext, key):
    ciphertext = ''
    matrix = create_table()
    plaintext_no_space = plaintext.replace(' ', '')
    keyText = ''
    index = 0

    for x in range(len(plaintext_no_space)):
        keyText += key[index:index+1]
        
        if index == len(key)-1:
            index = 0
        else:
            index+=1
    
    index = 0

    for i in range(len(plaintext)):
        if plaintext[i:i+1] == ' ':
            ciphertext += ' '
        else:
            row = (ord(keyText[index]) - ord('a')) / 2
            column = ord(plaintext_no_space[index]) - ord('a')

            ciphertext += matrix[int(row)][int(column)].decode('utf-8')
            if index == len(keyText)-1:
                index = 0
            else:
                index+=1
    
    return ciphertext

def main():
    plaintext = 'defend the walls of the castle'
    ciphertext = 'synnjs hwy bwpng mz lqv rzdmtn'
    key = 'fortify'
    p = encrypt(plaintext, key)
    print(p)
    p = encrypt(ciphertext, key)
    print(p)

main()