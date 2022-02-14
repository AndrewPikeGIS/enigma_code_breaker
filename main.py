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

test_enigma = enigma.EnigmaMachine(1, 2, 3, plug_board)

test_string = "test string"

test_enigma.string_in = test_string

test_enigma.print_string_in()

test_enigma.parse_string()

encrypted_string = test_enigma.encrypted_string

test_enigma.print_encrypted_string()

test_enigma.decrypt_string(encrypted_string, 1, 2, 3)

test_enigma.print_decrypted_string()

test_rotor = enigma.EnigmaRotor(1, 1, 1)

letters = string.ascii_lowercase

forward_eq_back = True

letterin = "b"
lettercryp = test_rotor.rotor_encryption_forward(letterin)
letterout = test_rotor.rotor_encryption_backward(lettercryp)

print(letterin)
print(lettercryp)
print(letterout)
print(test_rotor.get_rotor_pairs())
