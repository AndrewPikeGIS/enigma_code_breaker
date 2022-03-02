from sympy import E
from enigma_code.enigma_cypher_machine import EnigmaMachine


class Victory:
    def __init__(self):
        self.encrypted_message = ""

        self.build_enigma_machine()

    def read_encrypted_text(self, txt_path):
        with open(txt_path, "r") as txt_file:
            self.encrypted_message = txt_file.read()

        self.known_value = " " * len(self.encrypted_message)

    def build_enigma_machine(self):

        self.rotor1seed = 1
        self.rotor2seed = 1
        self.rotor3seed = 1

        self.rotor1start = 1
        self.rotor2start = 1
        self.rotor3start = 1

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

        self.Enigma = EnigmaMachine(plugboard, rotor1seed, rotor1start,
                                    rotor2seed, rotor2start, rotor3seed, rotor3start)

    def set_known_value(self, value, start_position):

        known_val = self.known_value

        length_replacement = len(value)

        known_val = known_val[:start_position] + value + \
            known_val[start_position + length_replacement:]

        self.known_value = known_val

    def check_output_on_known_val(self):
        # check the decrypted string against the known value string and give a score
        pass

    def decrypt_with_known_value(self):
        # code to decrypt the string when there are some known values.

        pass

    def interate_on_starting_positions(self):
        # iterate the enigma starting positions
        pass

    def iterate_on_rotor_seed(self):
        # iterate the enigma seeds
        pass

    def iterate_on_plugboard(self):
        # iterate the plugboard
        pass


VictoryTest = Victory()

VictoryTest.read_encrypted_text(r"encrypted_commands/command1.txt")

VictoryTest.set_known_value("Good Morning,\n\nWeather today", 0)

VictoryTest.set_known_value(
    "Hail Hitler.", len(VictoryTest.encrypted_message)-11)

print(VictoryTest.known_value)
