from pickle import TRUE
import pytest

import enigma_code_breaker.enigma_code.enigma_cypher_machine as enigma


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

# build test to make sure 26 vals and keys are created
