import pandas as pd
from enigma_code.enigma_cypher_machine import EnigmaMachine


class Victory:
    def __init__(self):
        self.encrypted_message = ""

        self.known_value = ""

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
        if self.Enigma.decrypted_string != "" and self.known_value != "":

            known_string = self.known_value

            decrypted_string = self.Enigma.decrypted_string

            counter = 0

            for x in range(len(known_string)):
                if decrypted_string[x] != " ":
                    if known_string[x] == decrypted_string[x]:
                        counter += 1

            self.decrypt_score = (counter/len(decrypted_string)) * 100
        elif self.known_value != "":
            print("Missing decrypted value. Please run decrypt_string() first.")
        elif self.known_value == "":
            print(
                "Known values missing. Please add known value with set_known_value() first.")

    def decrypt_string(self):
        # code to decrypt the string when there are some known values.
        self.Enigma.string_in = self.encrypted_message
        self.Enigma.decrypt_string()

    def interate_on_starting_positions(self):
        # iterate the enigma starting positions
        self.rotor1start += 1

        if self.rotor1start >= 26:
            self.rotor1start = 0
            self.rotor2start += 1
            if self.rotor2start >= 26:
                self.rotor3start = 0
                self.rotor3start += 1
                if self.rotor3start >= 26:
                    return("All possibilities checked")
        return(None)

    def iterate_on_rotor_seed(self):
        # iterate the enigma seeds
        pass

    def iterate_on_plugboard(self):
        # iterate the plugboard
        pass

    def iterate_on_reflector(self):
        # iterate on reflector
        pass

    def check_enigma_settings(self, number_of_iterations):

        for x in range(number_of_iterations):
            pass


VictoryTest = Victory()

VictoryTest.read_encrypted_text(r"encrypted_commands/command1.txt")

VictoryTest.set_known_value("Good Morning,\n\nWeather today", 0)

VictoryTest.set_known_value(
    "Hail Hitler.", len(VictoryTest.encrypted_message)-12)

VictoryTest.decrypt_string()

VictoryTest.check_output_on_known_val()

print(VictoryTest.known_value)

print(VictoryTest.Enigma.decrypted_string)

print(VictoryTest.decrypt_score)
