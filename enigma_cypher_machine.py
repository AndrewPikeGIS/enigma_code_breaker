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

    
class enigma_rotor:
    def __init__(self, rotor_position, starting_position, rotor_seed):
        
        self.rotor_position = rotor_position

        self.rotor_pairs = {}
        
        self.build_rotor_pairs(rotor = rotor_seed)
        
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
    
    def rotate_rotor(self):
        self.starting_position += 1
        
        if self.starting_position > 26:
            self.starting_position = 0

#for enigma class 
#string comes in, process one letter at a time.
#build three rotors, position right, left, center
#pass letter in to plug board, swap 10 pairs
#pass current letter into rotor 1
#pass letter to remaining rotor 2, 3, and reflector
#pas back through rotors 3,2,1
#pass back through plug board
#return the coded value.

class enigma_machine:
    def __init__(self, rotor1_start, rotor2_start, rotor3_start, reflector, plug_board) :
        
        self.rotor_1 = enigma_rotor(rotor_position = 1, starting_position = rotor1_start, rotor_seed= 1)
        
        self.rotor_2 = enigma_rotor(rotor_position = 2, starting_position = rotor2_start, rotor_seed= 2)
        
        self.rotor_3 = enigma_rotor(rotor_position = 3, starting_position = rotor3_start, rotor_seed= 3)
        



test = enigma_rotor(rotor_position = 1 , starting_position = 1, rotor_seed = 1)

print(test.rotor_position)

print(test.starting_position)

test.rotate_rotor()

print(test.starting_position)

print(test.rotor_pairs)