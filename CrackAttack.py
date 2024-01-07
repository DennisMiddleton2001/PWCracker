import hashlib, random, string, itertools, sys, md4
from itertools import permutations

def convert_text_to_hash(text_input, hash_type):
            # hashlib doesn't support md4, so we have to manually do it ourselves.
            
            if hash_type == 'md4':
                password = text_input.encode()
                # If you are scanning passwords in the SAM for a Windows machine, this is the way to crack the hash.
                h = md4.new()
                h.update(password)
                hash_string = h.digest().hex()
            else:
                password = text_input.encode()
                hash_string = hashlib.new(hash_type, password).hexdigest()
            return hash_string
         
def dictionary_attack(password_try_hash_string, hash_type, encoding):
    
    with open("dictionary.txt", 'r') as f:
        for line in f:
            password = line.strip()
            converted_hash = convert_text_to_hash(password, hash_type)
            #print('PW:  "' + password + '"     Hash: ' + converted_hash)
            if (converted_hash == password_try_hash_string):
                print(" ")
                print("Password is:  '" + password + "'")
                return True
        print("Not found")
        return False

def generate_brute_guess(alphanum):
    i = 0
    while True:
        result = itertools.product(alphanum, repeat=i)
        for guess in result:
            yield guess
        i += 1

def bruteforce(password_hash_string, hash_type, encoding):
    char_set = [chr(_) for _ in list(range(ord('a'), ord('z')+1))] + [chr(_) for _ in list(range(ord('0'), ord('9')+1))] + [chr(_) for _ in list(range(ord("{"), ord("~")+1))] + [chr(_) for _ in list(range(ord(' '), ord('~')+1))] + [chr(_) for _ in list(range(ord(' '), ord('/')+1))] + [chr(_) for _ in list(range(ord(':'), ord('@')+1))] + [chr(_) for _ in list(range(ord('['), ord('`')+1))]
    g = generate_brute_guess(char_set)
    for c in range(40000000000000):
            guess = (''.join(next(g)))
 #           print('G: ' + guess)
            password_try_hash = convert_text_to_hash(guess, hash_type)
            if password_hash_string == password_try_hash:                 
                 print(" ")
                 print("Password is:  '" + guess + "'")
                 return True
    return False

def main(opt, hash_type, argument, encoding):
    
    hash_string = convert_text_to_hash(argument, hash_type)

    if (opt == '-h'):
        print("Hash Value:  " + hash_string)
    elif (opt == '-p'):
         hash_string = argument.encode(encoding)
         print("Dictionary Attack...")
         if (dictionary_attack(argument, hash_type, encoding)==False):
             print("Brute Force Attack.")
             bruteforce(argument, hash_type, encoding)
    else:
         print("Invalid command line.")

if __name__ == '__main__':
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
    print('\n')

    # It's necessary to encode as a specific character type or the hash will not calculate the 
    # correct hash digest value. In Windows, it's usually 'utf-16le', but sometimes it's 'utf-8'.  
    # The difference is the number of bits that define the character.  For instance, 0x30 
    # in 'utf-8' is '0x0030' in utf16le.
    # This affects the calculation, so be sure to know what type of string you are passing to the
    # function.
    encoding = 'utf-16le'

    #Lines for debugging.
    hash_type = 'md5'
    #convert_text_to_hash("~1", hash_type)
    #bruteforce(convert_text_to_hash('~1', hash_type), hash_type, encoding)
    #main('-p', hash_type, "1f241085e8da2445c3131ed1ec93e9eb", encoding)

    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3], encoding)
    else:
         print("Usage:")
         print("  -p [hashtype] [hashvalue] search for hash.")
         print("  -h [hashtype] [password] print password hash.")
         print("\n")
         print("Supported hashtypes are:")
         print(" md4 - Windows/LM2")
         print(" md5")
         print(" sha1")
         print(" sha224")
         print(" sha256")
         print(" sha384")
         print(" sha512")
         print(" sha3_224")
         print(" sha3_256")
         print(" sha3_384")
         print(" sha3_512")
         print(" shake_128")
         print(" shake_256")
         print(" blake_2b")
         print(" blake_2s")
