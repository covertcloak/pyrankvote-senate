"""
Multiple seat ranking methods

Implemented methods:
 - Single transferable vote
 - Preferential block voting
"""

from typing import List
from pyrankvote.helpers import CompareMethodIfEqual, ElectionManager, ElectionResults
from pyrankvote.models import Candidate, Ballot
import math


def single_transferable_vote(
    candidates: List[Candidate],
    ballots: List[Ballot],
    number_of_seats: int,
    compare_method_if_equal=CompareMethodIfEqual.MostSecondChoiceVotes,
    pick_random_if_blank=False,
) -> ElectionResults:
    """
    Single transferable vote (STV) is a multiple candidate election method, that elected the candidate that can
    based on proportional representation. Minority groups therefore get representation.

    If only one candidate can be elected, this method is the same as Instant runoff voting.

    Voters rank candidates and are granted as one vote each. If a candidate gets more votes than the threshold for being
    elected, the candidate is proclaimed as winner. This function uses the Droop quota, where

        droop_quota = votes/(seats+1)

    If one candidate get more votes than the threshold the excess votes are transfered to voters that voted for this
    candidate's 2nd (or 3rd, 4th etc) alternative. If no candidate get over the threshold, the candidate with fewest votes
    are removed. Votes for this candidate is then transfered to voters 2nd (or 3rd, 4th etc) alternative.

    For more info see Wikipedia.
    """

    rounding_error = 1e-6

    manager = ElectionManager(
        candidates,
        ballots,
        number_of_votes_pr_voter=1,
        compare_method_if_equal=compare_method_if_equal,
        pick_random_if_blank=pick_random_if_blank,
    )
    election_results = ElectionResults()

    voters, seats = manager.get_number_of_non_exhausted_ballots(), number_of_seats
    votes_needed_to_win: float = voters / float((seats + 1)) + 1   # Droop quota

    # Remove worst candidate until same number of candidates left as electable
    # While it is more candidates left than electable
    NC_votes = 0

    while True:
        seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        candidates_in_race = manager.get_candidates_in_race()
        candidates_in_race_votes: List[float] = [
            manager.get_number_of_votes(candidate) for candidate in candidates_in_race
        ]
        for i, candidate in enumerate(candidates_in_race):
            if candidate.name == "No Confidence":
                NC_votes = candidates_in_race_votes[i]
        votes_remaining = sum(candidates_in_race_votes)
        last_votes = 0.0
        candidates_to_elect = []
        candidates_to_reject = []
        votes_needed_to_win = votes_remaining / float((seats_left+1)) + 1 # (Choice 1) Recalculate droop quota as per STV explanation iv
        print("new droop",votes_needed_to_win)



        for i, candidate in enumerate(candidates_in_race):
            votes_for_candidate = candidates_in_race_votes[i]
            is_last_candidate = i == len(candidates_in_race) - 1

            # Elect candidates with more votes than Droop quota
            if (votes_for_candidate - rounding_error) >= votes_needed_to_win:
                candidates_to_elect.append(candidate)

            # Reject candidates that even with redistribution can't change the results
            elif i >= seats_left and (votes_remaining - rounding_error) <= last_votes:
                if len(candidates_to_elect) > 0:
                    # Don't reject candidates if there are elected candidates that have not yet
                    # redistributed their votes
                    break
                else:
                    candidates_to_reject.append(candidate)

            elif is_last_candidate:
                # Should be caught by if statement above
                pass
                # raise RuntimeError("Illegal state")

            last_votes = votes_for_candidate
            votes_remaining -= votes_for_candidate

        for candidate in candidates_to_elect:
            manager.elect_candidate(candidate)

        for candidate in candidates_to_reject[::-1]:
            manager.reject_candidate(candidate)

        # If same number of seats left as there are candidates, elect all candidates
        # seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        # if manager.get_number_of_candidates_in_race() <= seats_left:
        #     for candidate in manager.get_candidates_in_race():
        #         candidates_to_elect.append(candidate)
        #         manager.elect_candidate(candidate)

        # If no seats left, reject the rest of the candidates
        seats_left = number_of_seats - manager.get_number_of_elected_candidates()
        if seats_left == 0:
            for candidate in manager.get_candidates_in_race()[::-1]:
                candidates_to_reject.append(candidate)
                manager.reject_candidate(candidate)

        # Register round result
        election_results.register_round_results(manager.get_results())

        # If all seats filled
        if manager.get_number_of_candidates_in_race() == 0:
            break

        else:
            # For voters who votes for elected candidates,
            # transfer excess votes to 2nd choice (or 3rd, 4th etc.)
            for candidate in candidates_to_elect:
                votes_for_candidate = manager.get_number_of_votes(candidate)
                excess_votes: float = votes_for_candidate - votes_needed_to_win
                print(candidate,excess_votes)
                manager.transfer_votes(candidate, excess_votes)

            # For votes who votes on rejected candidates,
            # transfer all votes to 2nd choice (or 3rd, 4th etc.)
            for candidate in candidates_to_reject:
                votes_for_candidate = manager.get_number_of_votes(candidate)
                manager.transfer_votes(candidate, votes_for_candidate)

            seats_left = number_of_seats - manager.get_number_of_elected_candidates()
            if len(candidates_in_race) <= seats_left and len(candidates_to_elect) == 0 and len(candidates_to_reject) == 0:

                candidates_in_race = manager.get_candidates_in_race()
                candidates_in_race_votes: List[float] = [
                    manager.get_number_of_votes(candidate) for candidate in candidates_in_race
                ]

                # uncomment below if NC should win at most 1 seat, keep commented if NC can deny people seats
                # NC_votes = 0 # if NC is elected, it has no "current votes"
                # for i, candidate in enumerate(candidates_in_race):
                #     if candidate.name == "No Confidence":
                #         NC_votes = candidates_in_race_votes[i]

                for i, candidate in enumerate(candidates_in_race):
                    votes_for_candidate = candidates_in_race_votes[i]
                    if votes_for_candidate > NC_votes:
                        candidates_to_elect.append(candidate)
                        print(candidate.name)
                    else:
                        candidates_to_reject.append(candidate)
                for candidate in candidates_to_elect:
                    manager.elect_candidate(candidate)
                for candidate in candidates_to_reject[::-1]:
                    manager.reject_candidate(candidate)
                election_results.register_round_results(manager.get_results())
                return election_results
            # New round
            continue

    return election_results

