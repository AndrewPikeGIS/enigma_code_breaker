import pytest

import enigma_code_breaker.enigma_code.enigma_cypher_machine as enigma


def test_plugboard():

    plugboard_test = {
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

    test_enigma = enigma.EnigmaMachine(1, 1, 1, plugboard_test)

    assert "t" in test_enigma.plug_board_pairs.keys()
    assert "j" not in test_enigma.plug_board_pairs.keys()
    assert "j" in test_enigma.plug_board_pairs.values()
