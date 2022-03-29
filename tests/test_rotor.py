from string import ascii_lowercase
import pytest

import enigma_code_breaker.enigma_code.enigma_cypher_machine as enigma

# test that rotating the rotor advances the positon.


def test_rotate():
    test_rotor = enigma.EnigmaRotor(1, 1, 1)
    test_rotor.rotate_rotor()

    assert test_rotor.position == 2


# test all enigma rotor configurations to ensure no val can be encoded as itself.

def test_no_matched_vals():
    matched_val = False

    for x in range(1, 6):
        test_rotor = enigma.EnigmaRotor(1, 1, x)

        rotor_pairs = test_rotor.rotor_pairs

        list_keys = list(rotor_pairs.keys())
        list_values = list(rotor_pairs.values())

        for x in range(len(rotor_pairs)):
            if list_keys[x] == list_values[x]:
                matched_val = True

    assert not matched_val

# test that the forward and backward string encrypt return the same value, for all input letters.


def test_rotor_forward_and_back_same_val():

    test_rotor = enigma.EnigmaRotor(1, 1, 1)

    letters = ascii_lowercase

    forward_eq_back = True

    for x in range(26):
        letterin = letters[x]
        lettercryp = test_rotor.rotor_encryption_forward(letterin)
        letterout = test_rotor.rotor_encryption_backward(lettercryp)

        if letterin != letterout:
            forward_eq_back = False
            print(letterin)
            print(letterout)

    assert forward_eq_back
