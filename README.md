# pyrankvote-senate
close implementation of STV rules used in CMU stugov 2026 election https://drive.google.com/file/d/1IEl8sQ5ONBF9ArDgcgahDJ09UuF2k2EP/view, adapted from https://github.com/jontingvold/pyrankvote/tree/390600133d02bbc1b3592825b122eecff536d1d8

## issues: 
- vii.2 is not implemented, but it's probably okay since fractional vote redistribution resulting in a tie when candidates were not previously tied seems crazy;
- unresolved interpretation of viii.1: 
  - When "No Confidence" is elected (due to being treated as a candidate as per ii.3), does it retain the votes it held when it won?
  - If so, a small number of no-confidence voters could theoretically prevent a government from being elected, even if a majority of voters are all in favor of the same candidates
  - If not, then "No Confidence" could win at most one seat, and a government could be formed while overriding the wishes of a majority that has no confidence in it
