"""
Results are not correct. Troubleshoot of the code is required
Inspired by : motarekk
Here i am trying to I apply the same idea of Create My_ceaser_cipherV1.py but on s-des
in encryption prosses:
The user can insert plaintext that want to cypher and the algorithm break down the entred text to several segments
cypher each one by one with random key and emplement he key in the ciphertext
in decryption prosses:
the algorithm find the key by the hint of place and delete both
then start decrypt by breaking down the entred binary to several segments
then converting the binary back to plaintext
the encrypt and decrypt prosses is totally wrong and i will fix it later
"""
import random
import binascii
binary_number = '0100100101'
def sdes_encrypt(plaintext) -> str:
    ciphertext = ''
    # converting Ptext to binary
    plaintext = ' '.join(format(ord(x), 'b') for x in plaintext)
    while True:
        part_to_remove = " "# remove spaces
        plaintext = plaintext.replace(part_to_remove, "")
        if part_to_remove not in plaintext:
            break
    split_list = []
    # Split the string into 8-character binarys
    for i in range(0, len(plaintext), 8):
        split_list.append(plaintext[i:i + 8])
    # Get the last string in the list
    last_string = split_list[-1]

    # Check if the length of the last string is less than 8
    if len(last_string) < 8:
        # Concatenate zeros to the end of the last string
        last_string += "0" * (8 - len(last_string))
    # Replace the last string in the list with the modified string
    split_list[-1] = last_string


    # subkey generation
    key = bin(random.getrandbits(10))[2:]

    while len(key) < 10:
        key = '0' + key

    keyf = binary_number + key

    subkeys = subkey_generation(key)
    for ptext in split_list:

        # initial permutation
        state = initial_permutation((ptext))

        # two rounds of feistel network
        for i in range(2):
            state = feistel(state, subkeys[i])
        # final permutation
        ciphertext += final_permutation(state)

    char_list = list(ciphertext)
    char_list.insert(9, keyf)# plcing key
    appended_string = ''.join(char_list)
    return appended_string


def sdes_decrypt(ciphertext) -> str:
    plaintext = ''
    #finding key
    index = ciphertext.find(binary_number)
    if index != -1 and index + 3 < len(ciphertext):  # finding key
        key = (ciphertext[index + 10:index + 20])
    ciphertext = ciphertext.replace(binary_number+key, "")
    # subkey generation
    subkeys = subkey_generation(key)
    #spliting the cypher
    split_list = []
    for i in range(0, len(ciphertext), 8):
        split_list.append(ciphertext[i:i + 8])

    for ctext in split_list:
        # initial permutation
        state = initial_permutation(ctext)

        # two rounds of feistel network
        for i in range(1, -1, -1):
            state = feistel(state, subkeys[i])

        # final permutation
        plaintext  += final_permutation(state)
        binary_string = ''
        plaint = ''
        cyphrt_colect = ''
    for i in range(0, len(plaintext), 7):
        cyphrt_colect = (plaintext[i:i + 7])
        decimal_integer = int(cyphrt_colect, 2)
        plaint += chr(decimal_integer)

    return plaint


def subkey_generation(key) -> list:
    # P10
    key = permutation_10(key)

    # divide
    L = key[:4]
    R = key[4:]

    # left shift by 1
    L = L[1:] + L[0]
    R = R[1:] + R[0]

    # generate first subkey
    subkey_1 = permutation_8(L + R)

    # left shift by 2
    L = L[1:] + L[0]
    R = R[1:] + R[0]

    # generate second subkey
    subkey_2 = permutation_8(L + R)

    subkeys = [subkey_1, subkey_2]

    return subkeys


def initial_permutation(plaintext):
    IP = [1, 5, 2, 0, 3, 7, 4, 6]
    permuted_text = ""
    for i in IP:
        permuted_text += plaintext[i]
    return permuted_text


def expand_permutation(R0) -> str:
    E_P = [3, 0, 1, 2, 1, 2, 3, 0]
    permuted_text = ""
    for i in E_P:
        permuted_text += R0[i]
    return permuted_text


def permutation_4(R0_F) -> str:
    P4 = [1, 3, 2, 0]
    permuted_text = ""
    for i in P4:
        permuted_text += R0_F[i]
    return permuted_text


def permutation_10(key):
    P10 = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
    permuted_key = ""
    for i in P10:
        permuted_key += key[i]
    permuted_key = pad(permuted_key,10)
    return permuted_key


def permutation_8(key):
    P8 = [5, 2, 6, 3, 7, 4, 9, 8]
    permuted_key = ""
    for i in P8:
        permuted_key += key[i]
    return permuted_key


def final_permutation(state):
    IP_1 = [3, 0, 2, 4, 6, 1, 7, 5]
    permuted_text = ""
    for i in IP_1:
        permuted_text += state[i]
    return permuted_text


def sbox_0(L) -> str:
    S0 = [['01', '11', '00', '11'], ['00', '10', '10', '01'], ['11', '01', '01', '11'], ['10', '00', '11', '10']]
    row = int(L[0] + L[3], 2)
    column = int(L[1] + L[2], 2)
    sboxed = S0[column][row]
    return sboxed


def sbox_1(R) -> str:
    S1 = [['00', '10', '11', '10'], ['01', '00', '00', '01'], ['10', '01', '01', '00'], ['11', '11', '00', '11']]
    row = int(R[0] + R[3], 2)
    column = int(R[1] + R[2], 2)
    sboxed = S1[column][row]
    return sboxed


def feistel(state, subkey) -> str:
    # divide state
    L0 = state[:4]
    R0 = state[4:]

    R1 = pad(xor(L0, F(R0, subkey)), 4)
    L1 = R0
    state = L1 + R1
    return state


def F(R0, subkey) -> str:
    # E/P
    R0_F = expand_permutation(R0)

    # XOR with subkey
    R0_F = pad(xor(R0_F, subkey), 8)

    # divide R0_F
    L = R0_F[:4]
    R = R0_F[4:]

    # s-box
    L = sbox_0(L)
    R = sbox_1(R)
    R0_F = L + R

    # P4
    R0_F = permutation_4(R0_F)
    return R0_F


# HELPER FUNCTIONS
def xor(a, b):
    return bin(int(a, 2) ^ int(b, 2)).replace('0b', '')


def pad(a, b):
    while len(a) < b:
        a = '0' + a
    return a

print("cypher or decypher?\n Enter 1 to cypher \n Enter 0 to decypher")
x = int(input("the numper: "))
if x ==1:
    plaintext= input("Enter the plantext: ")
    print(sdes_encrypt(plaintext))
else:
    ciphertext = input("Enter the cypher: ")
    print(sdes_decrypt(ciphertext))
