from doctest import testfile
import random
import string
import os

from sqlalchemy import null


# need to fix the random component so that it is repeatable.

class EnigmaRotor:
    def __init__(self, rotor_position, starting_position, rotor_seed):

        # position of rotor in enigma machine.
        self.rotor_position = rotor_position

        # rotor pairs
        self.rotor_pairs = {}

        # builds rotor pairs
        self.build_rotor_pairs(rotor=rotor_seed)

        # starting position for the rotor range 0-26
        self.position = starting_position

        # position where the rotor will force the neighboring rotor to rotate
        self.step_position = 0

        # sets the rotor positon based on the rotor seed.
        self.set_step_position(rotor_seed=rotor_seed)

    def build_rotor_pairs(self, rotor=1):
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
            values.append(pair[random.randint(0, len(pair)-1)])
            pair = letters

        self.rotor_pairs = dict(zip(keys, values))

    def get_rotor_pairs(self):
        return(self.rotor_pairs)

    def rotate_rotor(self):
        self.position += 1

        if self.position >= 26:
            self.position = 0

    def rotor_encryption_forward(self, char_in):
        letters = string.ascii_lowercase
        # get index positon of char_in
        index_in = letters.index(char_in)

        rotor_index = self.position
        rotor_pairs = self.rotor_pairs

        position_in_rotor = rotor_index + index_in

        if position_in_rotor >= 26:
            position_in_rotor -= 26

        char_out = list(rotor_pairs.values())[position_in_rotor]

        return(char_out)

    def rotor_encryption_backward(self, char_in):

        rotor_index = self.position
        rotor_pairs = self.rotor_pairs

        # get index positon of value that came out
        index_in = list(rotor_pairs.values()).index(char_in)

        position_in_rotor = index_in - rotor_index

        if position_in_rotor < 0:
            position_in_rotor += 26

        char_out = list(rotor_pairs.keys())[position_in_rotor]

        return(char_out)

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

    def check_position(self):
        if self.position >= 26:
            self.position = 25


class EnigmaMachine:
    def __init__(self, plug_board, rotor1_seed=1, rotor1_start=1, rotor2_seed=2, rotor2_start=1, rotor3_seed=3, rotor3_start=1):

        self.rotor_1 = EnigmaRotor(
            rotor_position=1, starting_position=rotor1_start, rotor_seed=rotor1_seed)

        self.rotor_2 = EnigmaRotor(
            rotor_position=2, starting_position=rotor2_start, rotor_seed=rotor2_seed)

        self.rotor_3 = EnigmaRotor(
            rotor_position=3, starting_position=rotor3_start, rotor_seed=rotor3_seed)

        self.reflector = {}

        self.plug_board_pairs = {}

        self.encrypted_string = ""

        self.decrypted_string = ""

        self.string_in = ""

        self.set_plug_board(plug_board)

        self.build_reflector()

    def build_reflector(self):
        keys = []
        values = []

        pair = string.ascii_lowercase

        random.seed(10)

        for x in range(13):
            keys.append(pair[0])
            pair = pair.replace(pair[0], "")
            for val in values:
                pair = pair.replace(val, "")
            val_add = pair[random.randint(0, len(pair)-1)]
            values.append(val_add)
            pair = pair.replace(val_add, "")

        self.reflector = dict(zip(keys, values))

    def set_plug_board(self, plug_board_pairs):
        if len(plug_board_pairs.keys()) <= 10:
            self.plug_board_pairs = plug_board_pairs
        else:
            print("MAXIMUM 10 PLUG BOARD SWITCHES")
            print("Call .set_plug_board() to try again.")

    def encrypt_char_plugboard(self, string_in):
        if string_in in self.plug_board_pairs.keys():
            string_out = self.plug_board_pairs[string_in]
        elif string_in in self.plug_board_pairs.values():
            vals = list(self.plug_board_pairs.values())
            string_out = list(self.plug_board_pairs.keys())[
                vals.index(string_in)
            ]
        else:
            string_out = string_in

        return(string_out)

    def encrypt_char_reflector(self, string_in):
        if string_in in self.reflector.keys():
            string_out = self.reflector[string_in]
        elif string_in in self.reflector.values():
            vals = list(self.reflector.values())
            string_out = list(self.reflector.keys())[
                vals.index(string_in)
            ]

        return(string_out)

    def parse_string(self, input_string="", direction="encrypt"):
        if direction == "encrypt":
            self.encrypted_string = ""
        else:
            self.decrypted_string = ""
        if direction == "encrypt":
            if input_string != "":
                self.string_in = input_string
            else:
                input_string = self.string_in
        else:
            if input_string != "":
                self.encrypted_string = input_string
            else:
                input_string = self.encrypted_string

        if input_string != "":
            if input_string[-4:] == ".txt":
                with open(input_string, "r") as txt_in:
                    text = txt_in.read()
                    for letter in text:
                        if letter.lower() in string.ascii_lowercase:
                            letter = letter.lower()
                            # run the encryption methods
                            self.encrypt_string(letter, direction)
                        else:
                            if direction == "encrypt":
                                self.encrypted_string += letter
                            else:
                                self.decrypted_string += letter
            else:
                for letter in input_string:
                    if letter.lower() in string.ascii_lowercase:
                        # run the encryption methods
                        letter = letter.lower()
                        self.encrypt_string(letter, direction)
                    else:
                        if direction == "encrypt":
                            self.encrypted_string += letter
                        else:
                            self.decrypted_string += letter

    def encrypt_string(self, string_in="", direction="encrypt"):
        if string_in == "":
            string_in = self.string_in

        if len(string_in) > 1:
            print("String length greater than 1 running through parse_string()")
            self.parse_string(string_in, direction=direction)
        else:

            # rotate rotors
            self.rotor_1.rotate_rotor()

            # rotate rotor 1, if position = rotate for rotor 1 then rotate 2
            if self.rotor_1.step_position == self.rotor_1.position:
                self.rotor_2.rotate_rotor()

            # if position = rotate for rotor 2 then rotate 3
            if self.rotor_2.step_position == self.rotor_2.position:
                self.rotor_3.rotate_rotor()

            # run current char through plugboard    functionalize more for testing.
            string_in = self.encrypt_char_plugboard(string_in)

            # run current char through rotor 1
            char_rotor1_out = self.rotor_1.rotor_encryption_forward(
                string_in
            )

            # run current char through rotor 2
            char_rotor2_out = self.rotor_2.rotor_encryption_forward(
                char_rotor1_out
            )

            # run current char through rotor 3
            char_rotor3_out = self.rotor_3.rotor_encryption_forward(
                char_rotor2_out
            )

            # run current char through reflector
            char_reflector_out = self.encrypt_char_reflector(
                char_rotor3_out
            )

            # pass back through rotors 3
            char_rotor3_b_out = self.rotor_3.rotor_encryption_backward(
                char_reflector_out
            )

            # pass back through rotor 2
            char_rotor2_b_out = self.rotor_2.rotor_encryption_backward(
                char_rotor3_b_out
            )

            # pass back through rotor 1
            char_rotor1_b_out = self.rotor_1.rotor_encryption_backward(
                char_rotor2_b_out
            )

            # pass back through plug board
            string_out = self.encrypt_char_plugboard(
                char_rotor1_b_out
            )

            if direction == "encrypt":
                self.encrypted_string += string_out
                return(string_out)
            else:
                self.decrypted_string += string_out
                return(string_out)

    def write_encrypted_string_to_text(self, path, name):
        txt_out = os.path.join(path, name + ".txt")

        with open(txt_out, "w") as txt:
            txt.write(self.encrypted_string)

    def decrypt_string(self,
                       rotor1_start=None,
                       rotor2_start=None,
                       rotor3_start=None,
                       string_in=""):

        direction = "decrypt"

        if rotor1_start is not None:
            self.rotor_1.position = rotor1_start
        if rotor2_start is not None:
            self.rotor_2.position = rotor2_start
        if rotor3_start is not None:
            self.rotor_3.position = rotor3_start

        if string_in == "":
            if self.encrypted_string is None:
                string_in = self.string_in
            else:
                string_in = self.encrypted_string

        if len(string_in) > 1:
            print("String length greater than 1 running through parse_string()")
            self.parse_string(string_in, direction=direction)
        else:
            self.decrypted_string = ""
            self.encrypt_string(string_in, direction=direction)

    def print_string_in(self):
        print("String to encrypt: " + self.string_in + "\n")

    def print_encrypted_string(self):
        print("Encrypted string: " + self.encrypted_string + "\n")

    def print_decrypted_string(self):
        print("Decrypted string: " + self.decrypted_string + "\n")

    def set_rotor_positons(self, rotor1=1, rotor2=1, rotor3=1):
        if rotor1 is not None:
            self.rotor_1.position = rotor1
        if rotor2 is not None:
            self.rotor_2.position = rotor2
        if rotor3 is not None:
            self.rotor_3.position = rotor3
