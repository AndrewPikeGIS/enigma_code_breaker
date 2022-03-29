import pytest
import pandas as pd

#import enigma_code_breaker.enigma_code.crack_enigma as crack_enigma
#from enigma_code.crack_enigma import Victory
import enigma_code_breaker.enigma_code.enigma_cypher_machine as enigma


def test_rank_best_plugboards():
    pd_test = pd.DataFrame({
        'score':          [1, 1, 5, 10, 25, 50, 2, 6, 10, 15, 20, 35, 60, 70, 80, 90, 69, 76, 58, 97, 65, 86, 94, 75, 98],
        'plugboard_seed': [1, 1, 1, 1, 2, 10, 2, 2, 3, 4, 4, 5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
    })

    refined_plug_seed_list = enigma.Victory.rank_best_plugboards(pd_test)

    assert refined_plug_seed_list == [1, 2, 3, 4, 5, 10]
