#enigma build
#entry string
#right hand rotor rotates
#plugboard swap for 10 pairs
#enter through entry wheel, military version did 1-1 but it is important for the entry into the wheels.
#pass through 3 rotors
#hit reflector scramble again.
#pass back through three rotors
#plug board swap for 10 same 10 pairs

from doctest import testfile
import random, string


#need to fix the random component so that it is repeatable.
    
class EnigmaRotor:
    def __init__(self, rotor_position, starting_position, rotor_seed):
        
        #position of rotor in enigma machine.
        self.rotor_position = rotor_position

        #rotor pairs
        self.rotor_pairs = {}
        
        #builds rotor pairs
        self.build_rotor_pairs(rotor = rotor_seed)
        
        #starting position for the rotor
        self.position = starting_position
        
        #position where the rotor will force the neighboring rotor to rotate
        self.step_position = 0
        
        #sets the rotor positon based on the rotor seed.
        self.set_step_position(rotor_seed = rotor_seed)
        
        
    def build_rotor_pairs(self, rotor = 1):
        keys = []
        values = []
        
        letters = string.ascii_lowercase
        pair = letters
        
        if rotor > 5 or rotor < 1:
            rotor = 5
        
        random.seed(rotor) 
        
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
        self.position += 1
        
        if self.position > 26:
            self.position = 0
        
    def set_step_position(self, rotor_seed):
        if rotor_seed >= 5 or rotor_seed < 1:
            self.step_position = 1
        elif rotor_seed == 4:
            self.step_position = 10
        elif rotor_seed == 3:
            self.step_position = 22
        elif rotor_seed == 2:
            self.step_position = 5
        else:
            self.step_position = 17
        



class EnigmaMachine:
    def __init__(self, rotor1_start, rotor2_start, rotor3_start, plug_board) :
        
        self.rotor_1 = EnigmaRotor(rotor_position = 1, starting_position = rotor1_start, rotor_seed= 1)
        
        self.rotor_2 = EnigmaRotor(rotor_position = 2, starting_position = rotor2_start, rotor_seed= 2)
        
        self.rotor_3 = EnigmaRotor(rotor_position = 3, starting_position = rotor3_start, rotor_seed= 3)
        
        self.reflector = EnigmaRotor(rotor_position = 5, starting_position = 1, rotor_seed = 5)
        
        self.plug_board_pairs = {}
        
        self.set_plug_board(plug_board)
    
    def set_plug_board(self, plug_board_pairs):
        if len(plug_board_pairs.keys()) <= 10:
            self.plug_board_pairs = plug_board_pairs
        else:
            print("MAXIMUM 10 PLUG BOARD SWITCHES")
            print("Call .set_plug_board() to try again.")
            
    def parse_string(self, input_string):

        if input_string[-4:] == ".txt":
            with open(input_string, "r") as txt_in:
                text = txt_in.read()
                for letter in text:
                    #run the encryption methods
                    self.encrypt_string(letter)
        else:
            for letter in input_string:
                #run the encryption methods      
                self.encrypt_string(letter)
    
    def rotor_encryption(self, char_in, rotor_in):
        letters = string.ascii_lowercase
        #get index positon of char_in
        index_in = letters.index(char_in)
        
        if rotor_in == 1:
            rotor_index = self.rotor_1.position
            rotor_pairs = self.rotor_1.rotor_pairs
        elif rotor_in == 2:
            rotor_index = self.rotor_2.position
            rotor_pairs = self.rotor_2.rotor_pairs
        else:
            rotor_index = self.rotor_3.position
            rotor_pairs = self.rotor_3.rotor_pairs
        
        
    
    def encrypt_string(self, string_in):
        
        if len(string_in) > 1:
            print("String length greater than 1 running through parse_string()")
            self.parse_string(string_in)
        else:
            #rotate rotors
            self.rotor_1.rotate_rotor()
            
            #rotate rotor 1, if position = rotate for rotor 1 then rotate 2
            if self.rotor_1.step_position == self.rotor_1.position:
                self.rotor_2.rotate_rotor()
            
            #if position = rotate for rotor 2 then rotate 3
            if self.rotor_2.step_position == self.rotor_2.position:
                self.rotor_3.rotate_rotor()
                
            #start processing string
            
            #run current char through plugboard
            if string_in in self.plug_board_pairs.keys():
                string_in = self.plug_board_pairs[string_in]
            
            print(string_in)
            
            #run current char through rotor 1
            
            
        
    
#initialize machine
 

#pass letter into associated index position of rotor 1 pass value out, 
#pass letter into associated index position of rotor 2 pass value out
#pass letter into associated index position of rotor 3 pass value out
#pass letter into associated index position of reflector pass value out.
#pass letter into associated index position of rotor 3 pass value out.
#pass letter into associated index position of rotor 2 pass value out
#pass letter into associated index position of rotor 1 pass value out
#pass letter back through plug board
#print to text or user.


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

test_enigma = EnigmaMachine(1, 2, 3, plug_board)

test_string = "test"

test_enigma.encrypt_string(test_string)

print(test_enigma.rotor_1.position)

#print(test_enigma.rotor_1.rotor_pairs)
