from typing import Set, Optional

from backend.main.objects.voter import Voter, BallotStatus, VoterStatus
from backend.main.objects.candidate import Candidate
from backend.main.objects.ballot import Ballot, generate_ballot_number
from backend.main.store.data_registry import VotingStore


def issue_ballot(voter_national_id: str) -> Optional[str]:
    """
    Issues a new ballot to a given voter. The ballot number of the new ballot. This method should NOT invalidate any old
    ballots. If the voter isn't registered, should return None.

    :params: voter_national_id The sensitive ID of the voter to issue a new ballot to.
    :returns: The ballot number of the new ballot, or None if the voter isn't registered
    """
    try:
        store = VotingStore.get_instance()
        isVoter = store.get_voter(voter_national_id)
        if isVoter is None:
            return None
        number_ballot = generate_ballot_number(voter_national_id)
        store.add_ballot(voter_national_id, number_ballot)
        return number_ballot
    except Exception as e:
        raise e


def count_ballot(ballot: Ballot, voter_national_id: str) -> BallotStatus:
    """
    Validates and counts the ballot for the given voter. If the ballot contains a sensitive comment, this method will
    appropriately redact the sensitive comment.

    This method will return the following upon the completion:
    1. [X] BallotStatus.FRAUD_COMMITTED - If the voter has already voted
    2. [X] BallotStatus.VOTER_BALLOT_MISMATCH - The ballot does not belong to this voter
    3. [X] BallotStatus.INVALID_BALLOT - The ballot has been invalidated, or does not exist
    4. [X] BallotStatus.BALLOT_COUNTED - If the ballot submitted in this request was successfully counted
    5. [X] BallotStatus.VOTER_NOT_REGISTERED - If the voter is not registered

    :param: ballot The Ballot to count
    :param: voter_national_id The sensitive ID of the voter who the ballot corresponds to.
    :returns: The Ballot Status after the ballot has been processed.
    """
    try:
        store = VotingStore.get_instance()
        # VOTER_NOT_REGISTERED
        voter = store.get_voter(voter_national_id)
        if voter is None:
            return BallotStatus.VOTER_NOT_REGISTERED
        # VOTER_BALLOT_MISMATCH
        is_ballot_to_voter = store.is_ballont_to_voter(
            voter_national_id, 
            ballot.ballot_number
        )
        if is_ballot_to_voter == 0:
            return BallotStatus.VOTER_BALLOT_MISMATCH
        # INVALID_BALLOT : is invalited
        is_ballot_invalidated = store.is_invalitated_ballot(ballot.ballot_number)
        print(is_ballot_invalidated)
        if is_ballot_invalidated > 0:
            return BallotStatus.INVALID_BALLOT
        # INVALID_BALLOT : does not exist
        is_existed_invalidated = store.is_existed_ballot(ballot.ballot_number)
        print(is_existed_invalidated)
        if is_existed_invalidated == 0:
            return BallotStatus.INVALID_BALLOT
        # FRAUD_COMMITTED
        cast_ballots =store.count_casted_ballot(voter_national_id)
        if cast_ballots > 0:
            store.update_status_voter(voter_national_id, str(VoterStatus.FRAUD_COMMITTED.value))
            store.invalidated_ballot(ballot.ballot_number)
            return BallotStatus.FRAUD_COMMITTED
        # BALLOT_COUNTED
        else:
            store.update_status_voter(voter_national_id, str(VoterStatus.BALLOT_COUNTED.value))
            store.validated_ballot(ballot.ballot_number)
            store.update_content_ballot(ballot.ballot_number, ballot.chosen_candidate_id ,ballot.voter_comments)
            return BallotStatus.BALLOT_COUNTED
    except Exception as e:
        raise e


def invalidate_ballot(ballot_number: str) -> bool:
    """
    Marks a ballot as invalid so that it cannot be used. This should only work on ballots that have NOT been cast. If a
    ballot has already been cast, it cannot be invalidated.

    If the ballot does not exist or has already been cast, this method will return false.

    :returns: If the ballot does not exist or has already been cast, will return Boolean FALSE.
              Otherwise will return Boolean TRUE.
    """
    try:
        store = VotingStore.get_instance()
        counting = store.is_invalitated_ballot(ballot_number)

        if counting > 0:
            return False
        else:
            store.invalidated_ballot(ballot_number)
            return True
    except Exception as e:
        raise e


def verify_ballot(voter_national_id: str, ballot_number: str) -> bool:
    """
    Verifies the following:

    1. That the ballot was specifically issued to the voter specified
    2. That the ballot is not invalid

    If all of the points above are true, then returns Boolean True. Otherwise returns Boolean False.

    :param: voter_national_id The id of the voter about to cast the ballot with the given ballot number
    :param: ballot_number The ballot number of the ballot that is about to be cast by the given voter
    :returns: Boolean True if the ballot was issued to the voter specified, and if the ballot has not been marked as
              invalid. Boolean False otherwise.
    """
    try:
        store = VotingStore.get_instance()
        counting = store.count_specified_validated_ballot(voter_national_id, ballot_number)

        if counting > 0:
            return True
        elif counting == 0:
            return False

    except Exception as e:
        raise e
    # TODO: Implement this!
    raise NotImplementedError()


#
# Aggregate API
#

def get_all_ballot_comments() -> Set[str]:
    """
    Returns a list of all the ballot comments that are non-empty.
    :returns: A list of all the ballot comments that are non-empty
    """
    # TODO: Implement this!
    raise NotImplementedError()


def compute_election_winner() -> Candidate:
    """
    Computes the winner of the election - the candidate that gets the most votes (even if there is not a majority).
    :return: The winning Candidate
    """
    try:
        store = VotingStore.get_instance()
        candidates = store.get_most_voted()
        return store.get_candidate(candidates[0][0])
    except Exception as e:
        raise e


def get_all_fraudulent_voters() -> Set[str]:
    """
    Returns a complete list of voters who committed fraud. For example, if the following committed fraud:

    1. first: "John", last: "Smith"
    2. first: "Linda", last: "Navarro"

    Then this method would return {"John Smith", "Linda Navarro"} - with a space separating the first and last names.
    """
    # TODO: Implement this!
    raise NotImplementedError()
