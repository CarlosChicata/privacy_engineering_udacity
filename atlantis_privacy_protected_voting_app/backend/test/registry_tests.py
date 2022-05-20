import pytest

import backend.main.api.registry as registry
from backend.main.objects.voter import Voter, VoterStatus
from backend.main.store.data_registry import VotingStore


class TestRegistry:
    def test_candidate_registration(self):
        """
        Checks to see if candidates are actually registered successfully
        """
        expected_candidate_names = {"Kathryn Collins", "Aditya Guha", "Rina Harvey"}
        for candidate_name in expected_candidate_names:
            registry.register_candidate(candidate_name)

        actual_candidates = registry.get_all_candidates()
        actual_candidate_names = set([candidate.name for candidate in actual_candidates])
        assert actual_candidate_names == expected_candidate_names

        for candidate in actual_candidates:
            assert registry.candidate_is_registered(candidate)

    def test_voter_registration(self):
        """
        Checks to see if the voters are actually registered successfully
        """
        all_voters = [
            Voter("Adam", "Smith", "111111111"),
            Voter("Thien", "Huynh", "222222222"),
            Voter("Neel", "Banerjee", "333333333"),
            Voter("Linda", "Qi", "444444444"),
            Voter("Shoujit", "Gande", "555555555"),
        ]

        for voter in all_voters:
            assert registry.get_voter_status(voter.national_id) == VoterStatus.NOT_REGISTERED
            assert registry.register_voter(voter), "Couldn't register {0} {1}".format(voter.first_name, voter.last_name)
            assert registry.get_voter_status(voter.national_id) == VoterStatus.REGISTERED_NOT_VOTED

    def test_different_format_national_id(self):
        """
        Check to see if a national id with a different format specified still works.
        """
        voter = Voter("Adam", "Smith", "111111111")
        same_voter = Voter("Adam", "Smith", "111-11-1111")

        assert registry.get_voter_status(voter.national_id) == VoterStatus.NOT_REGISTERED
        assert registry.get_voter_status(same_voter.national_id) == VoterStatus.NOT_REGISTERED
        assert registry.register_voter(voter), "Couldn't register {0} {1}".format(voter.first_name, voter.last_name)
        assert registry.register_voter(same_voter) is False, \
            "The exact same voter was recognized as a different voter".format(voter.first_name, voter.last_name)
        assert registry.get_voter_status(voter.national_id) == VoterStatus.REGISTERED_NOT_VOTED
        assert registry.get_voter_status(same_voter.national_id) == VoterStatus.REGISTERED_NOT_VOTED

    def test_de_register_voter(self):
        """
        Checks to see if voter de-registration is successful.
        """
        voter = Voter("Adam", "Smith", "111111111")
        assert registry.get_voter_status(voter.national_id) == VoterStatus.NOT_REGISTERED
        assert registry.register_voter(voter), "Couldn't register {0} {1}".format(voter.first_name, voter.last_name)
        assert registry.get_voter_status(voter.national_id) == VoterStatus.REGISTERED_NOT_VOTED
        assert registry.de_register_voter(voter.national_id), "Couldn't de-register {0} {1}".format(
            voter.first_name, voter.last_name)
        assert registry.get_voter_status(voter.national_id) == VoterStatus.NOT_REGISTERED

    @pytest.fixture(autouse=True)
    def clear_store_between_tests(self):
        VotingStore.refresh_instance()
