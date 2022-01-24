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
    keys = []
    values = []
    
    letters = string.ascii_lowercase
    pair = letters
    
    random.seed = rotor
    
    for x in range(26):
        keys.append(letters[x])
        pair = pair.replace(letters[x], "")
        for val in values:
            pair = pair.replace(val, "")
        values.append(pair[random.randint(0,len(pair)-1)])
        pair = letters
    
    dct_rotor_pairs = dict(zip(keys, values))
    
    return(dct_rotor_pairs)
    
class enigma_rotor:
    def __init__(self, position, rotor_num):
        self.position = position

        self.rotor_pairs = build_rotor_pairs(rotor_num)

test = enigma_rotor('right', build_rotor_pairs(1))

print(test.position)

print(test.rotor_pairs)