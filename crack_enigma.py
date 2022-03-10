
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
        for val in known_string[:]:
            if val.lower() not in ascii_lowercase:
                known_string.replace(val, "")
        length_known_inputs = len(known_string)
        self.matched_values = ""
        if self.decrypted_string != "" and self.known_value != "":

            known_string = self.known_value

            decrypted_string = self.decrypted_string

            counter = 0
            # update this so that only non space values are checked.
            for x in range(len(known_string)):
                if decrypted_string[x] in ascii_lowercase:
                    if known_string[x].lower() == decrypted_string[x]:
                        counter += 1
                        self.matched_values += known_string[x]
                    else:
                        self.matched_values += " "
                else:
                    self.matched_values += decrypted_string[x]

            self.decrypt_score = (
                counter/length_known_inputs) * 100
        elif self.known_value != "":
            print("Missing decrypted value. Please run decrypt_string() first.")
        elif self.known_value == "":
            print(
                "Known values missing. Please add known value with set_known_value() first.")

    def interate_on_starting_positions(self):
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
        self.rotor_1.position = self.rotor1_start
        self.rotor_2.position = self.rotor2_start
        self.rotor_3.position = self.rotor3_start

        return(return_val)

    def iterate_on_rotor_seed(self):
        # iterate the enigma seeds
        print("All rotor seeds checked")
        return("Done")

    def iterate_on_plugboard(self):
        if self.plugboard_seed != 100:
            self.plugboard_seed += 1
            self.build_plug_board()
        else:
            print("All plugboard combinations checked")
            return("Done")

    def iterate_on_reflector(self):
        # iterate on reflector
        if self.reflector_seed != 100:
            self.reflector_seed += 1
            self.build_reflector()
        else:
            print("All reflector combinations checked")
            return("Done")

    def store_decrypt_score(self, run_number):
        if self.decrypt_score > 10:
            new_score = pd.DataFrame(data={"run": [run_number], "rotor1_seed": [self.rotor_1.rotor_seed], "rotor2_seed": [self.rotor_2.rotor_seed], "rotor3_seed": [self.rotor_3.rotor_seed],
                                           "rotor1_start": [self.rotor1_start], "rotor2_start": [self.rotor2_start], "rotor3_start": [self.rotor3_start],
                                           "reflector": [self.reflector], "plugboard": [self.plug_board], "score": [self.decrypt_score], "known_value": [self.known_value],
                                           "decrypted_message": [self.decrypted_string], "matched_values": [self.matched_values], "encrypted_message": [self.encrypted_string], "reflector_seed": [self.reflector_seed]})

            concat_df = pd.concat(
                [self.score_table, new_score], ignore_index=True)

            self.score_table = concat_df

    def write_score_table(self):
        # update to only include scores above 50%?
        self.score_table.to_excel(
            "output/decrypt_score_" + str(self.number_of_iterations) + "_" + str(dt.date.today()) + ".xlsx")

    def hours_minutes_seconds(self, timedelta):
        days = timedelta.days
        seconds = timedelta.seconds
        hours = seconds//3600
        minutes = (seconds//60) % 60
        print("Time elapsed days:", days, "hours:",
              hours, "minutes:", minutes, "\n")

    def check_rotor_start_positions(self):
        iterate_start_return = ""
        print("Checking rotor start positions")
        while iterate_start_return != "Done" or self.decrypt_score < 100:
            self.decrypt_string()

            # check decrypted text with known val
            self.check_output_on_known_val()

            if self.decrypt_score == 100.0:
                break
            # store the decrypted values in the score dataframe
            self.store_decrypt_score(x)

            # iterate on start position
            iterate_start_return = self.interate_on_starting_positions()

    def print_percentage(self, run_count, number_of_iterations, current_status):
        percentage = (run_count/number_of_iterations)*100

        if percentage >= 10.0 and current_status == 0:
            print("10% complete")
            current_status += 10
        elif percentage >= 20.0 and current_status == 10:
            print("20% complete")
            current_status += 10
        elif percentage >= 30.0 and current_status == 20:
            print("30% complete")
            current_status += 10
        elif percentage >= 40.0 and current_status == 30:
            print("40% complete")
            current_status += 10
        elif percentage >= 50.0 and current_status == 40:
            print("50% complete")
            current_status += 10
        elif percentage >= 60.0 and current_status == 50:
            print("60% complete")
            current_status += 10
        elif percentage >= 70.0 and current_status == 60:
            print("70% complete")
            current_status += 10
        elif percentage >= 80.0 and current_status == 70:
            print("80% complete")
            current_status += 10
        elif percentage >= 90.0 and current_status == 80:
            print("90% complete")
            current_status += 10
        elif percentage >= 99.0 and current_status == 90:
            print("99% complete")
            current_status += 10

    def check_enigma_settings(self, number_of_iterations):
        time_start = dt.datetime.now()
        self.number_of_iterations = number_of_iterations
        # this may need to be changed to a while loop...
        while self.decrypt_score < 100:
            # decrypt the text

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


VictoryTest.check_enigma_settings(2000000)
