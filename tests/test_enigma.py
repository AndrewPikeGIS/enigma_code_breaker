from cgi import test
import pytest
from string import ascii_lowercase

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

    assert "f" in test_enigma.plug_board_pairs.keys()
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

# test that no duplicated values exist in plugboard


def test_no_duplicated_values_in_plugboard():
    plugboard_keys = list(test_enigma.plug_board_pairs.keys())
    plugboard_values = list(test_enigma.plug_board_pairs.values())

    assert len(set(plugboard_keys) & set(plugboard_values)) == 0

# test that reflector forward and backwards returns same result.

# test that forward backwards through plugboard and a rotor returns same letter.


def test_plug_to_rotor_and_back():
    string_in = "h"

    string_encrypt = test_enigma.encrypt_char_plugboard(string_in)

    # run current char through rotor 1
    char_rotor1_out = test_enigma.rotor_1.rotor_encryption_forward(
        string_encrypt
    )

    char_rotor1_back = test_enigma.rotor_1.rotor_encryption_backward(
        char_rotor1_out
    )

    string_out = test_enigma.encrypt_char_plugboard(char_rotor1_back)

    message = "P1: " + string_encrypt + "\nR1: " + char_rotor1_out + \
        "\nR1B: " + char_rotor1_back + "\nP1B: " + string_out

    assert string_in == string_out, message


def test_plug_to_rotor_to_reflector_back():
    letters = ascii_lowercase

    for string_char in letters:

        string_encrypt = test_enigma.encrypt_char_plugboard(string_char)

        # run current char through rotor 1
        char_rotor1_out = test_enigma.rotor_1.rotor_encryption_forward(
            string_encrypt
        )

        # run current char through reflector
        char_reflector_out = test_enigma.encrypt_char_reflector(
            char_rotor1_out
        )

        char_reflector_back = test_enigma.encrypt_char_reflector(
            char_reflector_out
        )

        char_rotor1_back = test_enigma.rotor_1.rotor_encryption_backward(
            char_reflector_back
        )

        string_out = test_enigma.encrypt_char_plugboard(char_rotor1_back)

        message = "P1: " + string_encrypt + "\nR1: " + char_rotor1_out + \
            "\nReF: " + char_reflector_out + "\nReB: " + char_reflector_back + \
            "\nR1B: " + char_rotor1_back + "\nP1B: " + string_out

        assert string_char == string_out, message


def test_plug_rotor_back():

    for string_char in ascii_lowercase:

        string_encrypt = test_enigma.encrypt_char_plugboard(string_char)

        # run current char through rotor 1
        char_rotor1_out = test_enigma.rotor_1.rotor_encryption_forward(
            string_encrypt
        )

        char_reflector = test_enigma.encrypt_char_reflector(
            char_rotor1_out
        )

        char_rotor1_back = test_enigma.rotor_1.rotor_encryption_backward(
            char_reflector
        )

        string_encrypted = test_enigma.encrypt_char_plugboard(char_rotor1_back)

        # send encrypted string back through workflow.

        string_encrypted_back = test_enigma.encrypt_char_plugboard(
            string_encrypted)

        # run current char through rotor 1
        char_rotor1_out_b = test_enigma.rotor_1.rotor_encryption_forward(
            string_encrypted_back
        )

        char_reflector_b = test_enigma.encrypt_char_reflector(
            char_rotor1_out_b
        )

        char_rotor1_back_b = test_enigma.rotor_1.rotor_encryption_backward(
            char_reflector_b
        )

        string_decrypted = test_enigma.encrypt_char_plugboard(
            char_rotor1_back_b)

        assert string_char == string_decrypted


# this will obviously fail right now...

def test_forward_back_encrypt():
    test_enigma = enigma.EnigmaMachine(1, 1, 1, plugboard_test)

    string_in = "h"

    test_enigma.string_in = string_in

    test_enigma.encrypt_string()

    # repopulates encrypted string with decrypted value.
    test_enigma.decrypt_string(1, 1, 1)

    assert string_in == test_enigma.decrypted_string


def test_reflector_values():

    test_reflector = test_enigma.reflector

    lst_test = list(test_reflector.keys()) + list(test_reflector.values())

    lst_test.sort()

    string_reflector = "".join(lst_test)

    assert ascii_lowercase == string_reflector
