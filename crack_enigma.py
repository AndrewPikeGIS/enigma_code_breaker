
from string import ascii_lowercase
import pandas as pd
from enigma_code.enigma_cypher_machine import EnigmaMachine
import datetime as dt


class Victory:
    def __init__(self):
        self.encrypted_message = ""

        self.known_value = ""

        self.matched_values = ""

        self.rotor1seed = 1
        self.rotor2seed = 1
        self.rotor3seed = 1
        self.rotor1start = 0
        self.rotor2start = 0
        self.rotor3start = 0
        self.reflectorseed = 10

        self.plugboard = {
            "a": "b",
            "c": "d",
            "e": "f",
            "g": "h",
            "i": "j",
            "k": "l",
            "m": "n",
            "o": "p",
            "q": "r",
            "s": "t"}

        self.score_table = pd.read_csv(r"data/decrypt_score.csv")

        self.build_enigma_machine()

    def read_encrypted_text(self, txt_path):
        with open(txt_path, "r") as txt_file:
            self.encrypted_message = txt_file.read()

        self.known_value = " " * len(self.encrypted_message)

    def build_enigma_machine(self):

        self.Enigma = EnigmaMachine(self.plugboard, self.rotor1seed, self.rotor1start,
                                    self.rotor2seed, self.rotor2start, self.rotor3seed, self.rotor3start, self.reflectorseed)

    def set_known_value(self, value, start_position):

        known_val = self.known_value

        length_replacement = len(value)

        known_val = known_val[:start_position] + value + \
            known_val[start_position + length_replacement:]

        self.known_value = known_val

    def check_output_on_known_val(self):
        # check the decrypted string against the known value string and give a score
        self.matched_values = ""
        if self.Enigma.decrypted_string != "" and self.known_value != "":

            known_string = self.known_value

            decrypted_string = self.Enigma.decrypted_string

            counter = 0
            # update this so that only non space values are checked.
            for x in range(len(known_string)):
                if decrypted_string[x] in ascii_lowercase:
                    if decrypted_string[x] != " ":
                        if known_string[x] == decrypted_string[x]:
                            counter += 1
                            self.matched_values += known_string[x]
                        else:
                            self.matched_values += " "
                    else:
                        self.matched_values += " "
                else:
                    self.matched_values += decrypted_string[x]

            self.decrypt_score = (
                counter/len(known_string.replace(" ", ""))) * 100
        elif self.known_value != "":
            print("Missing decrypted value. Please run decrypt_string() first.")
        elif self.known_value == "":
            print(
                "Known values missing. Please add known value with set_known_value() first.")

    def decrypt_string(self):
        # code to decrypt the string when there are some known values.
        self.Enigma.string_in = self.encrypted_message
        self.Enigma.decrypt_string()
        self.decrypted_string = self.Enigma.decrypted_string

    def interate_on_starting_positions(self):
        # iterate the enigma starting positions
        self.rotor1start += 1

        if self.rotor1start >= 26:
            self.rotor1start = 0
            self.rotor2start += 1
            if self.rotor2start >= 26:
                self.rotor2start = 0
                self.rotor3start += 1
                if self.rotor3start >= 26:
                    self.rotor1start = 0
                    self.rotor2start = 0
                    self.rotor3start = 0
                    return("Done")
        return("")

    def iterate_on_rotor_seed(self):
        # iterate the enigma seeds
        return("Done")

    def iterate_on_plugboard(self):
        # iterate the plugboard
        return("Done")

    def iterate_on_reflector(self):
        # iterate on reflector
        return("Done")

    def store_decrypt_score(self, run_number):
        new_score = pd.DataFrame(data={"run": [run_number], "rotor1_seed": [self.rotor1seed], "rotor2_seed": [self.rotor2seed], "rotor3_seed": [self.rotor3seed],
                                       "rotor1_start": [self.rotor1start], "rotor2_start": [self.rotor2start], "rotor3_start": [self.rotor3start],
                                       "reflector": [self.Enigma.reflector], "plugboard": [self.Enigma.plug_board_pairs], "score": [self.decrypt_score], "known_value": [self.known_value],
                                       "decrypted_message": [self.decrypted_string], "matched_values": [self.matched_values], "encrypted_message": [self.encrypted_message]})

        concat_df = pd.concat([self.score_table, new_score], ignore_index=True)

        self.score_table = concat_df

    def write_score_table(self):
        self.score_table.to_excel(
            "output/decrypt_score_" + str(self.number_of_iterations) + "_" + str(dt.date.today()) + ".xlsx")

    def hours_minutes_seconds(self, timedelta):

        days = timedelta.days
        seconds = timedelta.seconds
        hours = seconds//3600
        minutes = (seconds//60) % 60
        print("Time elapsed days:", days, "hours:",
              hours, "minutes:", minutes, "\n")

    def check_enigma_settings(self, number_of_iterations):
        time_start = dt.datetime.now()
        self.number_of_iterations = number_of_iterations
        print_count = 0
        # this may need to be changed to a while loop...
        for x in range(number_of_iterations):

            # decrypt the text
            self.decrypt_string()

            # check decrypted text with known val
            self.check_output_on_known_val()

            if self.decrypt_score == 100:
                break
            # store the decrypted values in the score dataframe
            self.store_decrypt_score(x)

            # iterate on start position
            iterate_start_return = self.interate_on_starting_positions()

            if iterate_start_return == "Done":
                # iterate on plugboard
                iterate_plug_return = self.iterate_on_plugboard()

                if iterate_plug_return == "Done":
                    # iterate on reflector
                    iterate_reflector_return = self.iterate_on_reflector()

                    if iterate_reflector_return == "Done":
                        # iterate on rotor seed
                        iterate_seed_return = self.iterate_on_rotor_seed()

                        if iterate_seed_return == "Done":
                            # all combinations checked.
                            print("All combinations checked\n")
                            break

            percentage = (x/number_of_iterations)*100

            if percentage >= 25.0 and print_count == 0:
                print("25% complete")
                print_count += 1
            elif percentage >= 50 and print_count == 1:
                print("50% complete")
                print_count += 1
            elif percentage >= 75 and print_count == 2:
                print("75% complete")
                print_count += 1
            elif percentage >= 99.0 and print_count == 3:
                print("99% complete")
                print_count += 1

        # store score in table
        self.write_score_table()

        score = self.score_table["score"]
        print("Max score found == " + str(score.max()))
        print("")

        delta_time = dt.datetime.now()-time_start
        self.hours_minutes_seconds(delta_time)
        print("Time per iteration:")
        print(delta_time/number_of_iterations)


VictoryTest = Victory()

VictoryTest.read_encrypted_text(r"encrypted_commands/command1.txt")

VictoryTest.set_known_value("Good Morning,\n\nWeather today", 0)

VictoryTest.set_known_value(
    "Hail Hitler.", len(VictoryTest.encrypted_message)-12)


VictoryTest.check_enigma_settings(20000)
