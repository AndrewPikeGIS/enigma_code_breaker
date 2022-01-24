#enigma build
#entry string
#right hand rotor rotates
#plugboard swap for 10 pairs
#enter through entry wheel
#pass through 3 rotors
#hit reflector scramble again.
#pass back through three rotors
#plug board swap for 10 same 10 pairs

import random, string

def build_rotor_pairs(rotor = 1):
    random.seed = rotor

    
    keys = []
    values = []
    
    letters = string.ascii_lowercase
    
    for x in range(26):
        keys.append(letters[x])
        values.append(random.choice(letters))
    
    
    dct_rotor_pairs = dict(zip(keys, values))
    
    return(dct_rotor_pairs)
    
class enigma_rotor:
    def __init__(self, position, rotor_pairs):
        self.position = position

        self.rotor_pairs = rotor_pairs

test = enigma_rotor('right', build_rotor_pairs(1))

print(test.position)

print(build_rotor_pairs())