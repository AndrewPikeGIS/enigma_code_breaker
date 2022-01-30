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


#need to fix the random component so that it is repeatable.
    
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
        
        random.seed(rotor) 
        
        #this doesn't work consistently
        
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

#fix this so that all combinations are included but only the edits are different
class enigma_plug_board:
    def __init__(self, plug_board_pairs):
        self.plug_board_pairs = {}
        
        self.set_plug_board(plug_board_pairs)
    
    def set_plug_board(self, plug_board_pairs):
        if len(plug_board_pairs.keys()) <= 10:
            self.plug_board_pairs = plug_board_pairs
        else:
            print("MAXIMUM 10 PLUG BOARD SWITCHES")
            print("Call .set_plug_board() to try again.")
      

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
    def __init__(self, rotor1_start, rotor2_start, rotor3_start, plug_board) :
        
        self.rotor_1 = enigma_rotor(rotor_position = 1, starting_position = rotor1_start, rotor_seed= 1)
        
        self.rotor_2 = enigma_rotor(rotor_position = 2, starting_position = rotor2_start, rotor_seed= 2)
        
        self.rotor_3 = enigma_rotor(rotor_position = 3, starting_position = rotor3_start, rotor_seed= 3)
        
        self.reflector = enigma_rotor(rotor_position = 5, starting_position = 1, rotor_seed = 5)
        
        self.plug_board = enigma_plug_board(plug_board)



plug_board = {
    "a" : "j",
    "g" : "k",
    "d" : "b",
    "t" : "f",
    "e" : "w",
    "h" : "a",
    "p" : "c",
    "o" : "r",
    "y" : "e",
    "n" : "g"
}    

test_enigma = enigma_machine(1, 2, 3, plug_board)

print(test_enigma.plug_board.plug_board_pairs)
