class Victory:
    def __init__(self):
        self.encrypted_message = ""

    def read_encrypted_text(self, txt_path):
        with open(txt_path, "r") as txt_file:
            self.encrypted_message = txt_file.read()
