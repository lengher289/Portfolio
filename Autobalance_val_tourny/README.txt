Weighted Sort for Team Formation

This script provides a method for forming teams in a gaming context based on player ranks and points. It includes two main functions:

generateTeams(numOfTeams, lsCap): Generates an initial team structure. It takes the number of teams and a list of team captains, returning a dictionary with teams as keys and captains as values.

weighted_sort(DataFrame): Takes a DataFrame with player information, ranks, and points. It aims to form balanced teams by allocating players with ranks and points. The function iterates through a set number of attempts (default: 10,000) to ensure fair team composition.

Please note that the script uses predetermined rank values and should ideally be enhanced to fetch player ranks from the Riot API for more accurate results. Additionally, it incorporates constraints for forming teams, including limits on the total points per team and the number of players per team.

To use this script, provide an Excel file with player data and ranks as 'inputs.xlsx'. Be aware that the script might require several attempts to achieve balanced teams. The final teams and player ranks are printed for evaluation.


Author: Leng Her