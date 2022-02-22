from cgi import print_environ, test
import enigma_code.enigma_cypher_machine as enigma
import string


plug_board = {
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

test_enigma = enigma.EnigmaMachine(1, 1, 1, plug_board)

test_string = "this may finally work"

test_enigma.string_in = test_string

test_enigma.print_string_in()

test_enigma.parse_string()

test_enigma.print_encrypted_string()

test_enigma.decrypt_string(1, 1, 1)

test_enigma.print_decrypted_string()

test_enigma.set_rotor_positons()
