# Valorant Tournament Team Balancer

## The problem

Running a Valorant tournament with mixed-skill players and pre-assigned captains, the
manual work of drafting balanced teams is tedious and the result is usually contested.
Everyone thinks their team got the short end. I wanted the assignment to be defensible:
teams balanced against a point budget rather than against someone's judgment.

## Approach

Each player carries a rank, and each rank maps to a point value. The balancer treats team
formation as a constraint satisfaction problem: assign every player to a team such that no
team exceeds the point cap and every team has the required roster size.

**`generateTeams(numOfTeams, lsCap)`** — builds the initial structure, mapping each team
to its captain.

**`weighted_sort(DataFrame)`** — takes player names, ranks, and points, then attempts
assignments until it finds one satisfying both the per-team point ceiling and the roster
size limit. Retries up to 10,000 times by default.

## Design notes

**Randomized retry rather than exact optimization.** This is a bin-packing variant, and
an exact solver would be the rigorous approach. For tournament sizes — a few dozen players
across a handful of teams — repeated random assignment converges fast enough that the
added complexity wasn't worth it. The tradeoff is that a very tight point cap can exhaust
the retry budget without finding a valid solution.

**Point caps over rank averaging.** Averaging ranks lets a team stack two very high
players against three low ones and still look balanced on paper. A hard point ceiling
prevents that shape.

## Limitations

- Rank values are hardcoded. Fetching live ranks from the Riot API would remove the manual
  data entry step and keep ranks current.
- May need several runs to land a valid configuration when constraints are tight — there's
  no feedback distinguishing "no solution exists" from "got unlucky."
- No role balancing. Teams are balanced on skill points only, not on agent roles or
  position preference.

## Running it

```
pip install pandas openpyxl
```

Provide `inputs.xlsx` in the project directory with player names, ranks, and points, then:

```
python Auto_Balance_Val.py
```

Final teams and player ranks print to console for review.

## Stack

Python, pandas
