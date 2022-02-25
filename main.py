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

test_enigma = enigma.EnigmaMachine(
    plug_board=plug_board, rotor1_start=2, rotor2_start=3, rotor3_start=1)

test_string = r"german_commands/command1.txt"

test_enigma.string_in = test_string

test_enigma.print_string_in()

test_enigma.parse_string()

test_enigma.print_encrypted_string()

#test_enigma.write_encrypted_string_to_text(r"encrypted_commands", "command1")

test_enigma.decrypt_string(2, 3, 1)

test_enigma.print_decrypted_string()
