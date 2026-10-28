import pyrankvote
from pyrankvote import Candidate, Ballot
import multi_seat_ranking_senate

college_seats = {"BXA":1,"CFA":6,"CIT":13,"DC":10,"MCS":6,"SCS":7,"TSB":5}

#BXA
# Create a Candidate object for each candidate `Candidate('Candidate Name')`
NoConfidence = Candidate('No Confidence')
# list all the candidates
candidates = [NoConfidence]
# For each ballot, create a Ballot object with list of candidates in the order they were ranked on their ballot `Ballot(ranked_candidates=[FirstChoice,SecondChoice,etc])`
ballots = [ Ballot(ranked_candidates=[NoConfidence])]
election_result = multi_seat_ranking_senate.single_transferable_vote(
    candidates, ballots, number_of_seats=college_seats["BXA"]
)
print("BXA ",election_result)

# CFA
Candidate1 = Candidate('Candidate 1')
Candidate2 = Candidate('Candidate 2')

candidates = [Candidate1, Candidate2, NoConfidence]

ballots = [
    Ballot(ranked_candidates=[Candidate1,Candidate2])
]

election_result = multi_seat_ranking_senate.single_transferable_vote(
    candidates, ballots, number_of_seats=college_seats["CFA"]
)
print("CFA ",election_result)

# SCS
candidates=[NoConfidence]

ballots = [

]

election_result = multi_seat_ranking_senate.single_transferable_vote(
    candidates, ballots, number_of_seats=college_seats["SCS"]
)
print("SCS ",election_result)

# TSB

candidates = [NoConfidence]

ballots = [

]

election_result = multi_seat_ranking_senate.single_transferable_vote(
    candidates, ballots, number_of_seats=college_seats["TSB"]
)
print("TSB ",election_result)

# CIT

candidates = []

ballots = [

]

election_result = multi_seat_ranking_senate.single_transferable_vote(
    candidates, ballots, number_of_seats=college_seats["CIT"]
)
print("CIT ",election_result)

# DC

candidates = []
ballots = [ ]
election_result = multi_seat_ranking_senate.single_transferable_vote(
    candidates, ballots, number_of_seats=college_seats["DC"]
)
print("DC ",election_result)

# MCS

candidates = []
ballots = []

election_result = multi_seat_ranking_senate.single_transferable_vote(
    candidates, ballots, number_of_seats=college_seats["MCS"]
)
print("MCS ",election_result)
