import enigma_cypher_machine as enigma


test_enigma = enigma.EnigmaMachine(
    plugboard_seed=10, rotor1_start=2, rotor2_start=3, rotor3_start=1, rotor1_seed=1, rotor2_seed=2, rotor3_seed=3, reflector_seed=10)

test_string = r"german_commands/command1.txt"

test_enigma.string_in = test_string

test_enigma.print_string_in()

test_enigma.parse_string()

test_enigma.print_encrypted_string()

test_enigma.write_encrypted_string_to_text(r"encrypted_commands", "command1")

test_enigma.decrypt_string(2, 3, 1)

test_enigma.print_decrypted_string()
