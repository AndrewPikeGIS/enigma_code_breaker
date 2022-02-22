from cgi import print_environ, test
import enigma_code.enigma_cypher_machine as enigma
import string


plug_board = {
    "a": "j",
    "g": "k",
    "d": "b",
    "t": "f",
    "e": "w",
    "h": "a",
    "p": "c",
    "o": "r",
    "y": "e",
    "n": "g"
}

test_enigma = enigma.EnigmaMachine(1, 2, 1, plug_board)

test_string = "test string"

test_enigma.string_in = test_string

test_enigma.print_string_in()

test_enigma.parse_string()

test_enigma.print_encrypted_string()

test_enigma.decrypt_string(1, 2, 1)

test_enigma.print_decrypted_string()

plugboard_test = {
    "a": "j",
    "b": "d",
    "c": "p",
    "e": "y",
    "f": "t",
    "g": "k",
    "h": "l",
    "i": "u",
    "m": "w",
    "o": "r",
}

test_enigma = enigma.EnigmaMachine(1, 1, 1, plugboard_test)

print(test_enigma.rotor_1.position)


string_char = "j"

print("string_in: " + string_char)

string_encrypt = test_enigma.encrypt_char_plugboard(string_char)

print("plugboard_return: " + string_encrypt)

# run current char through rotor 1
char_rotor1_out = test_enigma.rotor_1.rotor_encryption_forward(
    string_encrypt
)

print("rotor_return: " + char_rotor1_out)

char_reflector = test_enigma.encrypt_char_reflector(
    char_rotor1_out
)

print("reflector_return: " + char_reflector)

char_rotor1_back = test_enigma.rotor_1.rotor_encryption_backward(
    char_reflector
)

print("rotor_backward_return: " + char_rotor1_back)

string_encrypted = test_enigma.encrypt_char_plugboard(char_rotor1_back)

print("encrypted_string: " + string_encrypted)

# send encrypted string back through workflow.

string_encrypted_back = test_enigma.encrypt_char_plugboard(
    string_encrypted)

print("plug_return_d: " + string_encrypted_back)

# run current char through rotor 1
char_rotor1_out_b = test_enigma.rotor_1.rotor_encryption_forward(
    string_encrypted_back
)

print("rotor_return_d: " + char_rotor1_out_b)

char_reflector_b = test_enigma.encrypt_char_reflector(
    char_rotor1_out_b
)

print("reflector_return_d: " + char_reflector_b)

char_rotor1_back_b = test_enigma.rotor_1.rotor_encryption_backward(
    char_reflector_b
)

print("rotor_backward_return_d: " + char_rotor1_back_b)

string_decrypted = test_enigma.encrypt_char_plugboard(char_rotor1_back_b)

print("decrypted_string: " + string_decrypted)

print(test_enigma.rotor_1.position)

print(test_enigma.rotor_1.get_rotor_pairs())
