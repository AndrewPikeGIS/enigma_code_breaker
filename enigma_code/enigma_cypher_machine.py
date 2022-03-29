import random
import string
import os
import pandas as pd
import datetime as dt


# need to fix the random component so that it is repeatable.

class EnigmaRotor:
    def __init__(self, rotor_position, starting_position, rotor_seed):

        # position of rotor in enigma machine.
        self.rotor_position = rotor_position

        # rotor pairs
        self.rotor_pairs = {}

        # rotor seed
        self.rotor_seed = rotor_seed

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
    def __init__(self, plugboard_seed=10, rotor1_seed=1, rotor1_start=1, rotor2_seed=2, rotor2_start=1, rotor3_seed=3, rotor3_start=1, reflector_seed=10):

        self.rotor1_seed = rotor1_seed

        self.rotor1_start = rotor1_start

        self.rotor2_seed = rotor2_seed

        self.rotor2_start = rotor2_start

        self.rotor3_seed = rotor3_seed

        self.rotor3_start = rotor3_start

        self.reflector_seed = reflector_seed

        self.reflector = {}

        self.plug_board = {}

        self.plugboard_seed = plugboard_seed

        self.encrypted_string = ""

        self.decrypted_string = ""

        self.string_in = ""

        self.build_plug_board()

        self.build_reflector()

        self.build_rotors()

    def build_rotors(self):
        self.rotor_1 = EnigmaRotor(
            rotor_position=1, starting_position=self.rotor1_start, rotor_seed=self.rotor1_seed)

        self.rotor_2 = EnigmaRotor(
            rotor_position=2, starting_position=self.rotor2_start, rotor_seed=self.rotor2_seed)

        self.rotor_3 = EnigmaRotor(
            rotor_position=3, starting_position=self.rotor3_start, rotor_seed=self.rotor3_seed)

    def build_reflector(self):
        keys = []
        values = []

        pair = string.ascii_lowercase

        # starting case reflector seed between 0 -100
        if self.reflector_seed > 100:
            self.reflector_seed = 100
        elif self.reflector_seed < 0:
            self.reflector_seed = 0

        random.seed(self.reflector_seed)

        for x in range(13):
            keys.append(pair[0])
            pair = pair.replace(pair[0], "")
            for val in values:
                pair = pair.replace(val, "")
            val_add = pair[random.randint(0, len(pair)-1)]
            values.append(val_add)
            pair = pair.replace(val_add, "")

        self.reflector = dict(zip(keys, values))

    def build_plug_board(self):

        keys = []
        values = []

        pair = string.ascii_lowercase

        # starting case reflector seed between 0 -100
        if self.reflector_seed > 100:
            self.reflector_seed = 100
        elif self.reflector_seed < 0:
            self.reflector_seed = 0

        random.seed(self.plugboard_seed)

        for x in range(10):
            keys.append(pair[0])
            pair = pair.replace(pair[0], "")
            for val in values:
                pair = pair.replace(val, "")
            val_add = pair[random.randint(0, len(pair)-1)]
            values.append(val_add)
            pair = pair.replace(val_add, "")

        self.plug_board = dict(zip(keys, values))

    def encrypt_char_plugboard(self, string_in):
        if string_in in self.plug_board.keys():
            string_out = self.plug_board[string_in]
        elif string_in in self.plug_board.values():
            vals = list(self.plug_board.values())
            string_out = list(self.plug_board.keys())[
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


class Victory(EnigmaMachine):
    def __init__(self):
        self.encrypted_string = ""

        self.decrypted_string = ""

        self.known_value = ""

        self.matched_values = ""

        self.rotor1_seed = 1

        self.rotor2_seed = 2

        self.rotor3_seed = 3

        self.rotor1_start = 0

        self.rotor2_start = 0

        self.rotor3_start = 0

        self.reflector_seed = 0

        # self.plug_board = {
        #     "a": "b",
        #     "c": "d",
        #     "e": "f",
        #     "g": "h",
        #     "i": "j",
        #     "k": "l",
        #     "m": "n",
        #     "o": "p",
        #     "q": "r",
        #     "s": "t"}

        self.plugboard_seed = 0

        self.rotor_status = 0

        self.plugboard_status = 0

        self.reflector_status = 0

        self.rotor_seed_status = 0

        self.decrypt_score = 0

        self.refined_plugboard_seed_list = []

        self.score_table = pd.read_csv(r"data/decrypt_score.csv")

        self.build_reflector()

        self.build_plug_board()

        self.build_rotors()

    def read_encrypted_text(self, txt_path):
        with open(txt_path, "r") as txt_file:
            self.encrypted_string = txt_file.read()

        self.known_value = " " * len(self.encrypted_string)

    def set_known_value(self, value, start_position):

        known_val = self.known_value

        length_replacement = len(value)

        known_val = known_val[:start_position] + value + \
            known_val[start_position + length_replacement:]

        self.known_value = known_val

    def check_output_on_known_val(self):
        # check the decrypted string against the known value string and give a score
        known_string = self.known_value
        known_string = known_string.lower()

        length_known_inputs = len(
            known_string.replace(" ", "").replace("\n", "").replace(".", "").replace(",", "").replace("!", ""))
        self.matched_values = ""
        if self.decrypted_string != "" and known_string != "":

            decrypted_string = self.decrypted_string

            counter = 0

            for x in range(len(known_string)):
                if decrypted_string[x] in string.ascii_lowercase:
                    if known_string[x] == decrypted_string[x]:
                        counter += 1
                        self.matched_values += known_string[x]
                    else:
                        self.matched_values += " "
                else:
                    self.matched_values += decrypted_string[x]

            self.decrypt_score = (
                counter/length_known_inputs) * 100.0
        elif self.known_value != "":
            print("Missing decrypted value. Please run decrypt_string() first.")
        elif self.known_value == "":
            print(
                "Known values missing. Please add known value with set_known_value() first.")

    def brute_force_interate_on_starting_positions(self):
        # iterate the enigma starting positions

        return_val = ""
        self.rotor1_start += 1
        if self.rotor1_start >= 26:
            self.rotor1_start = 0
            self.rotor2_start += 1
            if self.rotor2_start >= 26:
                self.rotor2_start = 0
                self.rotor3_start += 1
                if self.rotor3_start >= 26:
                    self.rotor1_start = 0
                    self.rotor2_start = 0
                    self.rotor3_start = 0
                    return_val = "Done"
                    print("All rotor start positons checked")
        self.rotor_1.position = self.rotor1_start
        self.rotor_2.position = self.rotor2_start
        self.rotor_3.position = self.rotor3_start

        return(return_val)

    def brute_force_iterate_on_rotor_seed(self):
        # iterate the enigma seeds
        print("All rotor seeds checked")
        return("Done")

    def brute_force_iterate_on_plugboard(self):
        # iterate on plugboard
        if self.plugboard_seed != 10:
            self.plugboard_seed += 1
            self.build_plug_board()
        else:
            self.plugboard_seed = 0
            print("All plugboard combinations checked")
            return("Done")

    def rank_best_plugboards(dfscores):

        dfscores = dfscores.sort_values(by=['score'], ascending=False)

        dfscores = dfscores.head(20)

        list_plugboard_seeds = dfscores['plugboard_seed'].unique()

        list_plugboard_seeds.sort()

        return(list_plugboard_seeds)

    def intelligent_iterate_on_plugboard(self, total_iterations):
        if total_iterations < 26**3:
            if self.plugboard_seed != 10:
                self.plugboard_seed += 1
                self.build_plug_board()
            else:
                self.plugboard_seed = 0
                print("All plugboard combinations checked")
                return("Done")
        else:
            if len(self.refined_plugboard_seed_list) == 0:
                self.refined_plugboard_seed_list = self.rank_best_plugboards(
                    self.score_table)
                self.current_positon_in_refined_plug_list = 0
                self.plugboard_seed = self.refined_plugboard_seed_list[
                    self.current_positon_in_refined_plug_list]
                self.build_plug_board()
            elif (len(self.refined_plugboard_seed_list)-1) <= self.current_positon_in_refined_plug_list:
                self.current_positon_in_refined_plug_list += 1
                self.plugboard_seed = self.refined_plugboard_seed_list[
                    self.current_positon_in_refined_plug_list]
                self.build_plug_board()
            else:
                self.current_positon_in_refined_plug_list = 0
                self.plugboard_seed = self.refined_plugboard_seed_list[
                    self.current_positon_in_refined_plug_list]
                print("All plugboard combinations checked")
                return("Done")

        # plug board is a weak point in the design and can be exploited by limiting the plugboard seeds that are checked to ones with the highest score amongst a large enough sample set.
        # iterate on plugboard

        # if reflector ==2 calc highest plugboard and replace iterations to just list.

    def brute_force_iterate_on_reflector(self):
        # iterate on reflector
        if self.reflector_seed != 10:
            self.reflector_seed += 1
            self.build_reflector()
        else:
            self.reflector_seed = 0
            print("All reflector combinations checked")
            return("Done")

    def store_decrypt_score(self, run_number):
        if self.decrypt_score >= 0:
            new_score = pd.DataFrame(data={"run": [run_number], "rotor1_seed": [self.rotor_1.rotor_seed], "rotor2_seed": [self.rotor_2.rotor_seed], "rotor3_seed": [self.rotor_3.rotor_seed],
                                           "rotor1_start": [self.rotor1_start], "rotor2_start": [self.rotor2_start], "rotor3_start": [self.rotor3_start],
                                           "reflector": [self.reflector], "plugboard": [self.plug_board], "score": [self.decrypt_score], "known_value": [self.known_value],
                                           "decrypted_message": [self.decrypted_string], "matched_values": [self.matched_values], "encrypted_message": [self.encrypted_string],
                                           "reflector_seed": [self.reflector_seed], "plugboard_seed": [self.plugboard_seed]})

            concat_df = pd.concat(
                [self.score_table, new_score], ignore_index=True)

            self.score_table = concat_df

    def write_score_table(self):
        # update to only include scores above 50%?
        self.score_table.to_excel(
            "output/decrypt_score_" + str(dt.date.today()) + ".xlsx")

    def hours_minutes_seconds(self, timedelta):
        days = timedelta.days
        seconds = timedelta.seconds
        hours = seconds//3600
        minutes = (seconds//60) % 60
        print("Time elapsed days:", days, "hours:",
              hours, "minutes:", minutes, "\n")

    def print_percentage(self, run_count, number_of_iterations, current_status):
        percentage = (run_count/number_of_iterations)*100

        if percentage >= 25.0 and current_status == 0:
            print("25% complete")
            current_status += 25
        elif percentage >= 50.0 and current_status == 25:
            print("50% complete")
            current_status += 25
        elif percentage >= 75.0 and current_status == 50:
            print("75% complete")
            current_status += 25
        elif percentage >= 99.0 and current_status == 75:
            print("99% complete")
            current_status += 25

        return(current_status)

    # brute force algorithm for breaking the code
    def check_enigma_settings(self):
        time_start = dt.datetime.now()
        iterate_plug_return = ""
        iterate_reflector_return = ""
        iterate_seed_return = ""
        int_counter = 0
        total_iterations = 0
        current_status = 0
        number_of_iterations = 26**3
        # check rotor positions for initial plugboard, reflector and seed options.
        print("Checking rotor starting positions for plugboard seed:" +
              str(self.plugboard_seed) + " and reflector: " + str(self.reflector_seed))
        while self.decrypt_score < 100.0:
            total_iterations += 1
            int_counter += 1
            self.decrypt_string()

            # check decrypted text with known val
            self.check_output_on_known_val()

            # store the decrypted values in the score dataframe
            self.store_decrypt_score(total_iterations)

            # iterate on start position
            iterate_start_return = self.brute_force_interate_on_starting_positions()

            if iterate_start_return == "Done":

                iterate_plug_return = self.brute_force_iterate_on_plugboard()

                int_counter = 0
                current_status = 0

                if iterate_plug_return == "Done":
                    # iterate on reflector
                    iterate_reflector_return = self.brute_force_iterate_on_reflector()

                    if iterate_reflector_return == "Done":
                        # iterate on rotor seed
                        iterate_seed_return = self.brute_force_iterate_on_rotor_seed()

                        if iterate_seed_return == "Done":
                            # all combinations checked.
                            print("All combinations checked\n")
                            break

                print("Checked rotor starting positions for plugboard seed:" +
                      str(self.plugboard_seed) + " and reflector: " + str(self.reflector_seed))

            current_status = self.print_percentage(
                int_counter, number_of_iterations, current_status)

        # store score in table
        self.write_score_table()

        score = self.score_table["score"]
        print("Max score found == " + str(score.max()))
        print("")

        delta_time = dt.datetime.now()-time_start
        self.hours_minutes_seconds(delta_time)
        print("Time per iteration:")
        print(delta_time/total_iterations)
