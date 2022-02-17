import pytest

import enigma_code_breaker.enigma_code.enigma_cypher_machine as enigma

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

# test that values in plug board match input dct.


def test_plugboard():

    assert "t" in test_enigma.plug_board_pairs.keys()
    assert "j" not in test_enigma.plug_board_pairs.keys()
    assert "j" in test_enigma.plug_board_pairs.values()


def test_plugboard_in_same_as_reverse():
    string_in = "t"
    string_encrypted = test_enigma.encrypt_char_plugboard(string_in)
    string_out = test_enigma.encrypt_char_plugboard(string_encrypted)

    assert string_in == string_out

    string_in = "n"
    string_encrypted = test_enigma.encrypt_char_plugboard(string_in)
    string_out = test_enigma.encrypt_char_plugboard(string_encrypted)

    assert string_in == string_out

    string_in = "b"
    string_encrypted = test_enigma.encrypt_char_plugboard(string_in)
    string_out = test_enigma.encrypt_char_plugboard(string_encrypted)

    assert string_in == string_out

    string_in = "z"
    string_encrypted = test_enigma.encrypt_char_plugboard(string_in)
    string_out = test_enigma.encrypt_char_plugboard(string_encrypted)

    assert string_in == string_out


def test_no_duplicated_values_in_plugboard():
    plugboard_keys = list(test_enigma.plug_board_pairs.keys())
    plugboard_values = list(test_enigma.plug_board_pairs.values())

    assert len(set(plugboard_keys) & set(plugboard_values)) == 0
