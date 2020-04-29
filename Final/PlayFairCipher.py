def makeTable(key):
    alphabet = [False,False,False,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    size = 5
    matrix = [[0 for x in range(size)] for y in range(size)]
    place = 0
    spot = 0
    check = False
    for k in range(5):
        for i in range(5):
            if place < len(key):
                for j in range(place, len(key)):
                    c = key[j]
                    temp = ord(c)
                    tempInt = 96
                    if temp <= 122 and temp >= 97:
                        if not alphabet[temp-tempInt - 1]:
                            alphabet[temp - tempInt - 1] = True
                            matrix[k][i] = c
                            place += 1
                            check = True
                            break
                    place += 1
            if place >= len(key) and not check:
                for j in range(spot, 26):
                    if not alphabet[j]:
                        matrix[k][i] = chr(96 + j + 1)
                        spot += 1
                        break
                    spot += 1
            if check:
                check = False
    return matrix

def findChar(matrix, target):
    result = [0,0]
    for k in range(5):
        for i in range(5):
            if matrix[k][i] == target:
                result[0] = k
                result[1] = i
                return result
    return result

def encrypt(matrix, plainText):
    cipherText = ['0'] * len(plainText)
    first = '0'
    second = '0'
    temp1 = '0'
    temp2 = '0'
    firstIndex = 0
    check = False
    for k in range(len(plainText)):
        if plainText[k].isalpha() and plainText[k] != 'j' and plainText != 'J':
            if not check:
                temp1 = plainText[k]
                first = temp1.lower()
                firstIndex = k
                check = True
            else:
                temp2 = plainText[k]
                second = temp2.lower()
                index = findChar(matrix, first)
                row1 = index[0]
                col1 = index[1]
                index = findChar(matrix, second)
                row2 = index[0]
                col2 = index[1]
                if row1 == row2:
                    first = matrix[row1][(col1 + 1)%5]
                    second = matrix[row2][(col2 + 1)%5]
                elif col1 == col2:
                    first = matrix[(row1 + 1)%5][col1]
                    second = matrix[(row2 + 1)%5][col2]
                else:
                    first = matrix[row1][col2]
                    second = matrix[row2][col1]
                if temp1.isalpha() and temp1.isupper():
                    first = first.upper()
                if temp2.isalpha() and temp2.isupper():
                    second = second.upper()
                cipherText[firstIndex] = first
                cipherText[k] = second
                check = False
        else:
            cipherText[k] = plainText[k]
    if check and len(plainText) != 0:
        cipherText[len(cipherText) - 1] = '$'
    return cipherText

def decrypt(matrix, cipherText):
    plainText = ['0'] * len(cipherText)
    first = '0'
    second = '0'
    temp1 = '0'
    temp2 = '0'
    firstIndex = 0
    check = False
    for k in range(len(cipherText)):
        if cipherText[k].isalpha() and cipherText[k] != 'j' and cipherText != 'J':
            if not check:
                temp1 = cipherText[k]
                first = temp1.lower()
                firstIndex = k
                check = True
            else:
                temp2 = cipherText[k]
                second = temp2.lower()
                index = findChar(matrix, first)
                row1 = index[0]
                col1 = index[1]
                index = findChar(matrix, second)
                row2 = index[0]
                col2 = index[1]
                if row1 == row2:
                    first = matrix[row1][(col1 - 1)%5]
                    second = matrix[row2][(col2 - 1)%5]
                elif col1 == col2:
                    first = matrix[(row1 - 1)%5][col1]
                    second = matrix[(row2 - 1)%5][col2]
                else:
                    first = matrix[row1][col2]
                    second = matrix[row2][col1]
                if temp1.isalpha() and temp1.isupper():
                    first = first.upper()
                if temp2.isalpha() and temp2.isupper():
                    second = second.upper()
                plainText[firstIndex] = first
                plainText[k] = second
                check = False
        else:
            plainText[k] = cipherText[k]
    return plainText

def PLEncrypt(plainText, key):
    newKey = key.lower()
    matrix = makeTable(newKey)
    text = plainText
    count = 0
    for k in range(len(plainText)):
        if plainText[k].isalpha():
            count += 1
    if count%2 != 0:
        text = text + "Q"
    cipherText = encrypt(matrix, text)
    text = ''.join(cipherText)
    if len(text) > 0:
        if text[len(text) - 1] == '$':
            text = text[:-1]
    return text

def PLDecrypt(cipherText, key):
    newKey = key.lower()
    matrix = makeTable(newKey)
    plainText = decrypt(matrix, cipherText)
    text = ''.join(plainText)
    if len(text) > 0:
        if text[len(text) - 1] == 'Q':
            text = text[:-1]
    return text
