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

test_enigma = enigma.EnigmaMachine(1, 1, 1, plug_board)

test_string = "test string"

test_enigma.string_in = test_string

test_enigma.print_string_in()

test_enigma.parse_string()

test_enigma.print_encrypted_string()

test_enigma.decrypt_string(1, 1, 1)

test_enigma.print_decrypted_string()

test_enigma.set_rotor_positons(1, 1, 1)

test_string = "uet ea"

test_enigma.string_in = test_string

test_enigma.print_string_in()

test_enigma.parse_string()

test_enigma.print_encrypted_string()

test_enigma.decrypt_string(1, 1, 1)

test_enigma.print_decrypted_string()
