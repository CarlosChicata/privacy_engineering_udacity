from backend.main.objects.voter import Voter, decrypt_name


class TestMinimization:

    def test_voter_id_minimization_consistency(self):
        """
        Checks to make sure that the obfuscated voter ID is consistent across hashes
        """
        voter = Voter("Adam", "Smith", "111111111")
        minimal_voter = voter.get_minimal_voter()

        obfuscated_natl_id = minimal_voter.obfuscated_national_id

        for _ in range(10):
            current_obfuscated_natl_id = voter.get_minimal_voter().obfuscated_national_id
            assert obfuscated_natl_id == current_obfuscated_natl_id

    def test_voter_name_minimization_inconsistency(self):
        """
        Checks to make sure that the names are encrypted non-deterministically
        """
        voter = Voter("Adam", "Smith", "111111111")
        minimal_voter = voter.get_minimal_voter()

        obfuscated_first_name = minimal_voter.obfuscated_first_name
        obfuscated_last_name = minimal_voter.obfuscated_last_name

        for _ in range(10):
            current_minimal_voter = voter.get_minimal_voter()
            assert obfuscated_first_name != current_minimal_voter.obfuscated_first_name
            assert obfuscated_last_name != current_minimal_voter.obfuscated_last_name

            obfuscated_first_name = current_minimal_voter.obfuscated_first_name
            obfuscated_last_name = current_minimal_voter.obfuscated_last_name

    def test_name_encryption_reversibility(self):
        """
        Checks to see that name encryption is reversible.
        """
        for _ in range(10):
            voter = Voter("Adam", "Smith", "111111111")
            minimal_voter = voter.get_minimal_voter()

            decrypted_first_name = decrypt_name(minimal_voter.obfuscated_first_name)
            decrypted_last_name = decrypt_name(minimal_voter.obfuscated_last_name)

            assert voter.first_name == decrypted_first_name
            assert voter.last_name == decrypted_last_name


