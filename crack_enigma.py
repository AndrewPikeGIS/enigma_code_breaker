
from string import ascii_lowercase
import pandas as pd
from enigma_code.enigma_cypher_machine import EnigmaMachine
import datetime as dt


class Victory(EnigmaMachine):
    def __init__(self):
        self.encrypted_string = ""

        self.decrypted_string = ""

        self.known_value = ""

        self.matched_values = ""

        self.rotor1_seed = 1

        self.rotor2_seed = 1

        self.rotor3_seed = 1

        self.rotor1_start = 0

        self.rotor2_start = 0

        self.rotor3_start = 0

        self.reflector_seed = 0

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

        self.build_reflector(self.reflector_seed)

        self.set_plug_board(self.plugboard)

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
        self.matched_values = ""
        if self.decrypted_string != "" and self.known_value != "":

            known_string = self.known_value

            decrypted_string = self.decrypted_string

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

    def decrypt_message(self):
        # code to decrypt the string when there are some known values.
        self.string_in = self.encrypted_string
        self.decrypt_string()

    def interate_on_starting_positions(self):
        # iterate the enigma starting positions
        self.rotor_1.position += 1

        if self.rotor_1.position >= 26:
            self.rotor_1.position = 0
            self.rotor_2.position += 1
            if self.rotor_2.position >= 26:
                self.rotor_2.position = 0
                self.rotor_3.position += 1
                if self.rotor_3.position >= 26:
                    self.rotor_1.position = 0
                    self.rotor_2.position = 0
                    self.rotor_3.position = 0
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
        if self.reflector_seed != 100:
            self.reflector_seed += 1
        else:
            return("Done")

    def store_decrypt_score(self, run_number):
        new_score = pd.DataFrame(data={"run": [run_number], "rotor1_seed": [self.rotor_1.rotor_seed], "rotor2_seed": [self.rotor_2.rotor_seed], "rotor3_seed": [self.rotor_3.rotor_seed],
                                       "rotor1_start": [self.rotor_1.position], "rotor2_start": [self.rotor_2.position], "rotor3_start": [self.rotor_3.position],
                                       "reflector": [self.reflector], "plugboard": [self.plug_board_pairs], "score": [self.decrypt_score], "known_value": [self.known_value],
                                       "decrypted_message": [self.decrypted_string], "matched_values": [self.matched_values], "encrypted_message": [self.encrypted_string]})

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
            self.decrypt_message()

            # check decrypted text with known val
            self.check_output_on_known_val()

            if self.decrypt_score == 100.0:
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
    "Hail Hitler.", len(VictoryTest.encrypted_string)-12)


VictoryTest.check_enigma_settings(20000)
