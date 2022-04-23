#
# This file is the internal-only API that allows for the population of the voter registry.
# This API should not be exposed as a REST API for election security purposes.
#
from typing import List
from backend.main.objects.voter import Voter, VoterStatus
from backend.main.objects.candidate import Candidate
from backend.main.store.data_registry import VotingStore

#
# Voter Registration
#


def register_voter(voter: Voter) -> bool:
    """
    Registers a specific voter for the election. This method doesn't verify that the voter is eligible to vote or any
    such legal logistics -- it simply registers them if they aren't currently registered.

    :param: voter The voter to register.
    :returns: Boolean TRUE if the registration was successful. Boolean FALSE if the voter was already registered
              (based on their National ID)
    """
    # TODO: Implement this!
    try:
        store = VotingStore.get_instance()
        national_id = voter.national_id.replace("-", "").replace(" ", "").strip()
        first_name = voter.first_name.lower()
        last_name = voter.last_name.lower()
        proxy_voter = Voter(first_name, last_name, national_id)
        return store.add_voter(proxy_voter)
    except Exception as e:
        raise e



def get_voter_status(voter_national_id: str) -> VoterStatus:
    """
    Checks to see if the specified voter is registered.

    :param: voter_national_id The sensitive ID of the voter to check the registration status of.
    :returns: The status of the voter that best describes their situation
    """
    try:
        store = VotingStore.get_instance()
        status = store.get_status_voter(voter_national_id.replace("-", "").replace(" ", "").strip())
        if status is None or str(VoterStatus.NOT_REGISTERED.value) == status:
            return VoterStatus.NOT_REGISTERED
        elif str(VoterStatus.BALLOT_COUNTED.value) == status:
            return VoterStatus.BALLOT_COUNTED
        elif str(VoterStatus.FRAUD_COMMITTED.value) == status:
            return VoterStatus.FRAUD_COMMITTED
        elif str(VoterStatus.REGISTERED_NOT_VOTED.value) == status:
            return VoterStatus.REGISTERED_NOT_VOTED
        else: return status
    except Exception as e:
        raise e
    # TODO: Implement this!
    raise NotImplementedError()


def de_register_voter(voter_national_id: str) -> bool:
    """
    De-registers a voter from voting. This is to be used when the user requests to be removed from the system.
    If a voter is a fraudulent voter, this should still be reflected in the system; they should not be able to
    de-registered.

    :param: voter_national_id The sensitive ID of the voter to de-register.
    :returns: Boolean TRUE if de-registration was successful. Boolean FALSE otherwise.
    """
    try:
        store = VotingStore.get_instance()
        clean_national_id = voter_national_id.replace("-", "").replace(" ", "").strip()
        status = store.get_status_voter(clean_national_id)
        if str(VoterStatus.FRAUD_COMMITTED.value) == status:
            return False
        else:
            return store.delete_voter(clean_national_id)
    except Exception as e:
        raise e


#
# Candidate Registration (Already Implemented)
#

def register_candidate(candidate_name: str):
    """
    Registers a candidate for the election, if not already registered.
    """
    store = VotingStore.get_instance()
    store.add_candidate(candidate_name)


def candidate_is_registered(candidate: Candidate) -> bool:
    """
    Checks to see if the specified candidate is registered.

    :param: candidate The candidate to check the registration status of
    :returns: Boolean TRUE if the candidate is registered. Boolean FALSE otherwise.
    """
    store = VotingStore.get_instance()
    return store.get_candidate(candidate.candidate_id) is not None


def get_all_candidates() -> List[Candidate]:
    store = VotingStore.get_instance()
    return store.get_all_candidates()
