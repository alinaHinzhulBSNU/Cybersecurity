import hashlib
import itertools
import time


# For input data
def validation(word, symbols):
    for symbol in word:
        if symbol not in symbols:
            return False
    return True


# Decrypt by hash
def brute_force(hash, symbols, repeat=0):
    for sequence in itertools.product(symbols, repeat=repeat):
        word_try = ''.join(sequence)
        if hashlib.sha3_384(word_try.encode()).hexdigest() == hash:
            return word_try

    return brute_force(hash, symbols, repeat + 1)


if __name__ == '__main__':
    # Data
    all_letters = [chr(n) for n in range(ord('a'), ord('z') + 1)]
    all_digits = [chr(n) for n in range(ord('0'), ord('9') + 1)]
    symbols = all_letters + all_digits

    message = input("Input message (only lower case letters and digits): ")
    while not validation(message, symbols):
        message = input("Input message (only lower case letters and digits): ")

    # Hash
    hash = hashlib.sha3_384(message.encode()).hexdigest()  # Can be used as a signature
    print("Hash: %s" % hash)

    # Brute forcing
    print("Brute-forcing...")
    start = time.time()
    result = brute_force(hash, symbols)
    end = time.time()
    runtime = end - start
    print("Runtime: %s seconds" % runtime)
    print("Brute-force result: %s" % result)