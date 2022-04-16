import string
from random import choice

import backend.main.api.balloting as balloting
import backend.main.api.registry as registry
from backend.main.objects.voter import Voter


class TestPrivacySanity:
    """
    These tests don't guarantee that your implementation protects privacy, but if they fail, it's likely that your
    code doesn't protect privacy.
    """

    def test_national_id_minimization_non_inclusion(self):
        """
        Checks to make sure that the national id is not included in the obfuscated version of the national id
        """
        for _ in range(10):
            national_id = TestPrivacySanity.generate_random_national_id()
            voter = Voter("Adam", "Smith", national_id)
            obfuscated_national_id = voter.get_minimal_voter().obfuscated_national_id

            assert national_id not in obfuscated_national_id
            assert obfuscated_national_id not in national_id

    def test_national_id_minimization_ordering(self):
        """
        The orders of national ids and obfuscated national ids shouldn't match
        """
        ascending_ordered_national_ids = sorted([TestPrivacySanity.generate_random_national_id() for _ in range(10)])

        # Preserves the order
        obfuscated_national_ids = [
            Voter("Some", "Voter", national_id).get_minimal_voter().obfuscated_national_id
            for national_id in ascending_ordered_national_ids
        ]

        # Now, sort the obfuscated national ids
        ascending_ordered_obfuscated_national_ids = sorted(obfuscated_national_ids)
        descending_ordered_obfuscated_national_ids = reversed(sorted(obfuscated_national_ids))

        # Make sure the orders don't match
        assert ascending_ordered_obfuscated_national_ids != obfuscated_national_ids
        assert descending_ordered_obfuscated_national_ids != obfuscated_national_ids

    def test_ballot_number_non_inclusion(self):
        """
        Ensures that the ballot number doesn't include either the obfuscated national id, or the original national id
        itself (and vice-versa).
        """
        for _ in range(10):
            national_id = TestPrivacySanity.generate_random_national_id()
            voter = Voter("Some", "Voter", national_id)
            registry.register_voter(voter)
            obfuscated_national_id = voter.get_minimal_voter().obfuscated_national_id

            for __ in range(5):
                ballot_number = balloting.issue_ballot(voter.national_id)

                # Check for National Id leaks
                assert national_id not in ballot_number
                assert ballot_number not in national_id

                # Don't want the obfuscated one either because then anyone can associate them together with the voter
                assert obfuscated_national_id not in ballot_number
                assert ballot_number not in obfuscated_national_id

    def test_ballot_number_ordering(self):
        """
        It shouldn't be apparently which ballot was issued after another ballot -- there should be no rhyme in ordering
        """
        for _ in range(10):
            national_id = TestPrivacySanity.generate_random_national_id()
            voter = Voter("Some", "Voter", national_id)
            registry.register_voter(voter)

            ballot_numbers_in_creation_order = [balloting.issue_ballot(voter.national_id) for _ in range(10)]
            ballot_numbers_in_ascending_order = sorted(ballot_numbers_in_creation_order)
            ballot_numbers_in_descending_order = reversed(sorted(ballot_numbers_in_creation_order))

            assert ballot_numbers_in_creation_order != ballot_numbers_in_ascending_order
            assert ballot_numbers_in_creation_order != ballot_numbers_in_descending_order

    @staticmethod
    def generate_random_national_id():
        return ''.join(choice(string.digits) for _ in range(9))
