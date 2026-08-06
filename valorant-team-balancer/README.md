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

## Design decisions

**The rank-to-point scale is non-linear, and deliberately so.** The obvious approach is to
number the ranks 1 through 25 and call it done. That's wrong, because the skill gap between
adjacent ranks isn't constant. Iron to Bronze is a much narrower real difference than
Diamond to Ascendant, and at the top of the ladder the distribution compresses — Immortal
and Radiant are close enough in practical terms that treating them as widely separated
tiers overweights a distinction that doesn't change how a team plays.

A linear scale would inflate spread at the bottom and flatten it at the top, producing
teams that look balanced on paper and aren't. The hardcoded values encode the actual shape
of the skill curve instead. There's also real variance within a rank — a Silver player can
perform at a Gold level on a given night — so the scale is deliberately coarse rather than
claiming a precision the underlying signal doesn't support.

**Point caps over rank averaging.** Averaging ranks lets a team stack two very high players
against three low ones and still look balanced. A hard point ceiling prevents that shape.

**Randomized retry rather than exact optimization.** This is a bin-packing variant, and an
exact solver would be the rigorous approach. For tournament sizes — a few dozen players
across a handful of teams — repeated random assignment converges fast enough that the added
complexity wasn't worth it. The tradeoff is that a very tight point cap can exhaust the
retry budget without finding a valid solution.

## Limitations

- **Rank entry is manual.** Pulling current ranks from the Riot API would remove the data
  entry step and keep ranks fresh. The rank-to-point mapping would stay as-is — that's a
  modeling choice, not missing data.
- **The point scale is untested against outcomes.** It reflects my read of the skill curve,
  not a fit to actual match results. With enough tournament data you could tune the values
  against observed team win rates.
- **No feedback on infeasibility.** Exhausting the retry budget doesn't distinguish "no
  valid assignment exists" from "got unlucky." Detecting infeasibility up front would be a
  real improvement.
- **No role balancing.** Teams are balanced on skill points only, not agent roles or
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
