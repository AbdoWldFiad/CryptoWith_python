'''
Here i am trying my idea 
insteded of the user should hold the chypherd text and key
this cypher will implement the key directly in the text 
and in decyphering prosses the algorithms will detect the key and bruteforce it to fing the right key
then it will dechipher the massege
let me explane how
In caeser function the key is set randomly and incrypt a 3 litter word with it firstly
then incrypt the plan text as any ceacer cipher
then implement the 3 litter cipher word with indication before it and print the cihperd text
in the caesar_deci function the code will try to find the indication to get the row key
the code then bruteforce it untille it find the original 3 litter word and save the key number 
then remove the indication and the row key and decipher the cipher text and finally print it
'''
import random

alfa = "abcdefghijklmnopqrstuvwxyz"
def caesar(Ptext):
    cipherT = " "
    cipherkey = "xdfxdf" # 112 bits
    key = random_number = random.randint(0, 25)#randoming key
    half = round(len(Ptext)/2)
    while True:
        part_to_remove = " "# more interferans
        Ptext = Ptext.replace(part_to_remove, "hxh")
        if part_to_remove not in Ptext:
            break
    for l in Ptext:
        if l not in alfa:
            cipherT += l
        else:# encription
            cipherT += alfa[(alfa.index(l) + key) % 26]
    for l in "abd":
       cipherkey += alfa[(alfa.index(l)+key)% 26]
    char_list = list(cipherT)# encripting key
    char_list.insert(half, cipherkey)# plcing key
    appended_string = ''.join(char_list)
    return appended_string

def caesar_deci (cipherT):
    given_string = "abd"
    decy_plenT = " "
    index = cipherT.find("xdfxdf")
    if index != -1 and index + 3 < len(cipherT):#finding key
        row_key = (cipherT[index + 6:index + 9])

    for l in range(1, 25):
        for shift in range(26):
            shifted_string = ""
            for letter in given_string:
                shifted_letter = chr((ord(letter) - 97 + shift) % 26 + 97)
                shifted_string += shifted_letter
            if shifted_string == row_key:#encouding key
                key = shift
    part_to_remove = "xdfxdf"
    cipherT = cipherT.replace(part_to_remove+row_key, "")

    for i in cipherT:
        if i not in alfa:
            decy_plenT += i
        else:
            decy_plenT += alfa[(alfa.index(i) - key) % 26]#encoding
    while True:
        part_to_remove = "hxh"
        decy_plenT = decy_plenT.replace(part_to_remove, " ")#less interfirance
        if part_to_remove not in decy_plenT:
            break
    return decy_plenT
# INPUTS
print("cypher or decypher?\n Enter 1 to cypher \n Enter 0 to decypher")
x = int(input("the numper: "))
if x ==1:
    Ptext = input("Enter the plantext: ")
    print(caesar(Ptext))
else:
    cipherT = input("Enter the cypher: ")
    print(caesar_deci(cipherT))
