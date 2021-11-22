import string
import traceback


# ENCRYPT
def vigenere_encrypt(alphabet, text, key):
    text_list = list(prepare_text(text))
    key_list = key * (len(text) // len(key)) + key[:(len(text) % len(key))]

    cipher = list()
    for index in range(len(text_list)):
        text_letter_index = alphabet.index(text_list[index])
        key_letter_index = alphabet.index(key_list[index])
        alphabet_letter_number = (text_letter_index + key_letter_index) % len(alphabet)
        cipher.append(alphabet[alphabet_letter_number])

    return "".join(cipher)


# DECRYPT
def vigenere_decrypt(alphabet, cipher, key):
    cipher_list = list(cipher)
    key_list = key * (len(cipher) // len(key)) + key[:(len(cipher) % len(key))]

    text = list()
    for index in range(len(cipher_list)):
        cipher_letter_index = alphabet.index(cipher_list[index])
        key_letter_index = alphabet.index(key_list[index])
        alphabet_letter_number = (cipher_letter_index - key_letter_index) % len(alphabet)
        text.append(alphabet[alphabet_letter_number])

    return "".join(text)


# TEXT VALIDATION
def prepare_text(text):
    return text.replace(' ', '')


# KEY VALIDATION
def valid_key(alphabet, key):
    for letter in key:
        if letter not in alphabet:
            return False
    return True


# READ FROM FILE
def read_from_file(path):
    with open(path, "r") as file:
        return file.read()


# WRITE TO FILE
def write_to_file(path, data):
    with open(path, "w") as file:
        file.write(data)


if __name__ == '__main__':
    try:
        # Alphabet (English)
        alphabet = list(string.ascii_lowercase)

        # Input
        input_path = input("Input path to source file: ")
        input_value = read_from_file(input_path)

        # Key
        key_value = input("Input key: ")
        while not valid_key(alphabet, key_value):
            key_value = input("Input key (the previous value is invalid): ")

        # Output
        output_path = input("Input path to result file: ")

        # Mode
        mode = input("\nSelect mode: \n\t 1 - Encryption mode \n\t 2 - Decryption mode\n")
        if mode == "1":
            result = vigenere_encrypt(alphabet, input_value, key_value)
            write_to_file(output_path, result)
            print("\nText is '" + input_value + "'")
            print("Key is '" + key_value + "'")
            print("Cipher is '" + result + "'")
            print("\nCipher has been written to the file " + output_path)
        elif mode == "2":
            result = vigenere_decrypt(alphabet, input_value, key_value)
            write_to_file(output_path, result)
            print("\nText is '" + result + "'")
            print("Key is '" + key_value + "'")
            print("Cipher is '" + input_value + "'")
            print("\nText has been written to the file " + output_path)
        else:
            print("Invalid mode!")

    except Exception as e:
        print("ERROR!!!\n" + traceback.format_exc())