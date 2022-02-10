from pickle import TRUE
import pytest

import enigma_code_breaker.enigma_code.enigma_cypher_machine as enigma


def test_rotate():
    test_rotor = enigma.EnigmaRotor(1, 1, 1)
    test_rotor.rotate_rotor()

    assert test_rotor.position == 2
