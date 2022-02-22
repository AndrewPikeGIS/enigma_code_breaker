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

test_enigma = enigma.EnigmaMachine(3, 24, 15, plug_board)

test_string = "test string"

test_enigma.string_in = test_string

test_enigma.print_string_in()

test_enigma.parse_string()

encrypted_string = test_enigma.encrypted_string

test_enigma.print_encrypted_string()

test_enigma.decrypt_string(encrypted_string, 3, 24, 15)

test_enigma.print_decrypted_string()

test_reflector = test_enigma.reflector

lst_test = list(test_reflector.keys()) + list(test_reflector.values())

lst_test.sort()

print("".join(lst_test))
