from cs50 import get_string
import sys

def main():
    if len(sys.argv) != 2:
        print("missing command-line argument, or ONLY enter one word")
        exit(1)
    if sys.argv[1].isalpha()==False:
        print ("keyword not all alphabetic")
        exit(1)
    if sys.argv[1].isalpha()==True:
        print("keyword alphabetic. enter plaintext to encipher")


    plaintext = get_string()

    print("ciphertext: ",end="")
    keyword = sys.argv[1]

    keylength = len(keyword)
    counter = 0

    for c in plaintext:
        if c.isalpha() == False:
            print(c, end="")
        else:
            if c.isupper():
                cipher = keyword[counter % keylength].upper()
                ciphernum = ord(cipher.upper()) if cipher.islower() else ord(cipher)
                print (chr(((ord(c) - ord('A')) + (ciphernum - ord('A'))) % 26 + ord('A')),end="")
            else:
                cipher = keyword[counter % keylength]
                ciphernum = ord(cipher.lower()) if cipher.isupper() else ord(cipher)
                print (chr(((ord(c) - ord('a')) + (ciphernum - ord('a'))) % 26 + ord('a')),end="")
            counter += 1
    print('\n')
    exit(0)


if __name__ == "__main__":
    main()









