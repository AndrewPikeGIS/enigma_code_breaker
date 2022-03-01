class Victory:
    def __init__(self):
        self.encrypted_message = ""

        self.test = ""

    def read_encrypted_text(self, txt_path):
        with open(txt_path, "r") as txt_file:
            self.encrypted_message = txt_file.read()

    def __check_private(self):
        self.test = self.encrypted_message.upper()


VictoryTest = Victory()

VictoryTest.read_encrypted_text(r"encrypted_commands/command1.txt")

print(VictoryTest.test)
