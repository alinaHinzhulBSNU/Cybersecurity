import traceback
import time
import itertools
import os
import win32com.client as win32
import exrex
import english_words


# Returns True if password is correct for given file. Otherwise returns False
def password_is_correct(application: win32.CDispatch, path: str, password: str):
    try:
        application.Documents.Open(path, False, True, None, password)
        return True
    except Exception:
        return False


# Password brute forcing
def password_brute_force(application: win32.CDispatch, path: str, symbols: list):
    repeat = 1
    while True:
        for sequence in itertools.product(symbols, repeat=repeat):
            password_variant = ''.join(sequence)
            if password_is_correct(application, path, password_variant):
                return password_variant
        repeat = repeat + 1


# Mask attack
def password_mask_attack(application: win32.CDispatch, path: str, mask: str):
    passwords = list(exrex.generate(mask))
    for password_variant in passwords:
        if password_is_correct(application, path, password_variant):
            return password_variant
    return None


# Dictionary attack
def password_dictionary_attack(application: win32.CDispatch, path: str, dictionary: list):
    for password_variant in dictionary:
        if password_is_correct(application, path, password_variant):
            return password_variant
    return None


if __name__ == '__main__':
    try:
        print("\tRECOVER MS WORD FILE PASSWORD:")

        # Open application (MS Word)
        word_app = win32.Dispatch('Word.Application')
        word_app.Visible = True  # Look through file content

        # Path to file
        word_file_path = input("Enter path to MS Word file: ")
        if not os.path.exists(word_file_path):  # Check file existence
            raise FileNotFoundError

        # SELECT MODE
        mode = input("Select mode:\n\t1 - Brute force\n\t2 - Mask attack\n\t3 - Dictionary attack\n")

        # BRUTE FORCE
        if mode == "1":
            # SCOPE: Password symbols - latin letters and digits
            all_letters = [chr(n) for n in range(ord('a'), ord('z') + 1)]
            all_digits = [chr(n) for n in range(ord('0'), ord('9') + 1)]
            symbols = all_letters + all_digits

            # Brute forcing
            print("Brute-forcing...")

            start = time.time()
            password = password_brute_force(word_app, word_file_path, symbols)
            end = time.time()
            runtime = round((end - start) / 60, 2)  # in minutes

            print("Runtime: %s minutes" % runtime)
            print("Recovered password is '" + password + "'")

        # MASK ATTACK
        elif mode == "2":
            mask = input("Input password mask (regex): ")

            print("Mask attack...")
            start = time.time()
            password = password_mask_attack(word_app, word_file_path, mask)
            end = time.time()
            runtime = round((end - start) / 60, 2)  # in minutes

            if password is not None:
                print("Runtime: %s minutes" % runtime)
                print("Recovered password is '" + password + "'")
            else:
                print("Wrong regular expression!")

        # DICTIONARY ATTACK
        elif mode == "3":
            # SCOPE: English words
            dictionary = sorted(english_words.english_words_alpha_set)

            print("Dictionary attack...")
            start = time.time()
            password = password_dictionary_attack(word_app, word_file_path, dictionary)
            end = time.time()
            runtime = round((end - start) / 60, 2)  # in minutes

            if password is not None:
                print("Runtime: %s minutes" % runtime)
                print("Recovered password is '" + password + "'")
            else:
                print("Wrong dictionary!")

        # INVALID MODE
        else:
            print("Invalid mode!")

    except Exception as ex:
        print(traceback.format_exc())
