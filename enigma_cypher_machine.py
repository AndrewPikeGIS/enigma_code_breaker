#enigma build
#entry string
#right hand rotor rotates
#plugboard swap for 10 pairs
#enter through entry wheel, military version did 1-1 but it is important for the entry into the wheels.
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
    def __init__(self, rotor_position, starting_position):
        
        self.rotor_position = rotor_position

        self.rotor_pairs = {}
        
        self.starting_position = starting_position
        
    def build_rotor_pairs(self, rotor = 1):
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
        
        self.rotor_pairs = dict(zip(keys, values))
        
    def get_rotor_pairs(self):
        return(self.__rotor_pairs)



test = enigma_rotor('right', 1)

print(test.rotor_position)

test.build_rotor_pairs(1)

print(test.rotor_pairs.values())