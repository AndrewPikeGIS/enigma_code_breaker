import enigma_code.enigma_cypher_machine as enigma


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

test_enigma.print_encrypted_string()
