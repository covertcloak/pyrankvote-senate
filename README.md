# pyrankvote-senate
close implementation of [STV rules used in CMU stugov 2026 election](https://drive.google.com/file/d/1IEl8sQ5ONBF9ArDgcgahDJ09UuF2k2EP/view), adapted from [pyrankvote](https://github.com/jontingvold/pyrankvote/blob/master/pyrankvote/multiple_seat_ranking_methods.py)

## issues: 
- vii.2 is not implemented, but it's probably okay since fractional vote redistribution resulting in a tie when candidates were not previously tied seems unlikely;
- unresolved interpretation of viii.1: 
  - When "No Confidence" is elected (due to being treated as a candidate as per ii.3), does it retain the votes it held when it won?
  - If so, a small number of no-confidence voters could theoretically prevent a government from being elected, even if a majority of voters are all in favor of the same candidates
  - If not, then "No Confidence" could win at most one seat, and a government could be formed while overriding the wishes of a majority that has no confidence in it

## Recommendations for changes to the policy:
- remove vii.2 since it is atypical of STV and gives extra voting power to people who voted for more popular candidates 
- Use the exact [Droop Quota](https://en.wikipedia.org/wiki/Droop_quota) (total votes / (k + 1)) (change `votes_needed_to_win` in `multi_seat_ranking_senate.py`)
- Do not allow "No Confidence" to be ranked at all because it creates a lot of complexity in the system and undefined behavior. It does not make sense for a candidate who received votes not to receive an open seat.
