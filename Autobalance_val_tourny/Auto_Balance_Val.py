import random
import pandas as pd
import math



"""

Weighted Sort for Team Formation

This script provides a method for forming teams in a gaming context based on player ranks and points. It includes two main functions:

generateTeams(numOfTeams, lsCap): Generates an initial team structure. It takes the number of teams and a list of team captains, returning a dictionary with teams as keys and captains as values.

weighted_sort(DataFrame): Takes a DataFrame with player information, ranks, and points. It aims to form balanced teams by allocating players with ranks and points. The function iterates through a set number of attempts (default: 10,000) to ensure fair team composition.

Please note that the script uses predetermined rank values and should ideally be enhanced to fetch player ranks from the Riot API for more accurate results. Additionally, it incorporates constraints for forming teams, including limits on the total points per team and the number of players per team.

To use this script, provide an Excel file with player data and ranks as 'inputs.xlsx'. Be aware that the script might require several attempts to achieve balanced teams. The final teams and player ranks are printed for evaluation.

"""




#TODO: Modify Function, takes in 3 lists, (List of Player Rank,List of Player Name, List of Points associated with Rank)
        #Returns a DataFrame
        #Use this function and pass it into weighted_sort(DataFrame)

#TODO: Use riot api to get ranks instead of using self reported ranks. Create flags for potiential smurfs.


rank_vals = {'Iron1': 9.235, 'Iron2': 10.295, 'Iron3': 11.4749, 
'Bronze1': 12.7879, 'Bronze2': 14.2483, 'Bronze3': 15.8722, 
'Silver1': 17.6771, 'Silver2': 19.6819, 'Silver3': 21.9078, 
'Gold1': 24.3776, 'Gold2': 27.1161, 'Gold3': 30.1503, 
'Platinum1': 33.5093, 'Platinum2': 37.2244, 'Platinum3': 41.3291, 
'Diamond1': 45.8593, 'Diamond2': 50.8528, 'Diamond3': 56.3494, 
'Ascendant1': 62.3906, 'Ascendant2': 69.0194, 'Ascendant3': 76.2796, 
'Immortal1': 84.2155, 'Immortal2': 92.8711, 'Immortal3': 102.2893, 
'Radiant': 112.5105}



df = pd.read_excel("inputs.xlsx", sheet_name = "Data")

for index, value in enumerate(df["Rank"]):
    for key in rank_vals:
        if value == key:
            real = rank_vals[key]
            df.at[index,"Points"] = real

df = df.sort_values("Points" , ascending= False)


def generateTeams(numOfTeams,lsCap):
    dic = {}
    for i in range(numOfTeams):
        dic["Team"+str(i+1)] = [lsCap[i]]
    return dic

def weighted_sort(DataFrame):#Takes in dataframe TODO: Take another input of how many teams

    total_points = sum(DataFrame["Points"])#
    balanced = total_points/8 #set ideal value for 8 teams 
    kinda_bal = balanced + 4
    cp_df = DataFrame.copy()

    teams = {
        "Team1":[],
        "Team2":[],
        "Team3":[],
        "Team4":[],
        "Team5":[],
        "Team6":[],
        "Team7":[],
        "Team8":[]
    }

    Ranks = {
        "Team1":[],
        "Team2":[],
        "Team3":[],
        "Team4":[],
        "Team5":[],
        "Team6":[],
        "Team7":[],
        "Team8":[]
    }
    team1 = 0
    team2 = 0
    team3 = 0
    team4 = 0
    team5 = 0
    team6 = 0
    team7 = 0
    team8 = 0
    
    counts = 0

    already_picked = []#already picked players store the index of said player in list

    while True:
        
        index = random.randint(0, 39)
        
        while index in already_picked:#check to see if already in list
            index = random.randint(0, 39)#pick a random number to select random player
            


        player_info = DataFrame.iloc[index]#get player information from DataFrame

        temp1 = team1 + player_info[2]#Create temp variables used for comparison
        temp2 = team2 + player_info[2]
        temp3 = team3 + player_info[2]
        temp4 = team4 + player_info[2]
        temp5 = team5 + player_info[2]
        temp6 = team6 + player_info[2]
        temp7 = team7 + player_info[2]
        temp8 = team8 + player_info[2]


            
        if (temp1 <= balanced or temp1 <= kinda_bal) and len(teams["Team1"]) < 5 and index not in already_picked:#Constraints for team

            teams["Team1"].extend([player_info[1]])
            Ranks["Team1"].extend([player_info[0]])
            team1 = team1 + player_info[2]#actually add team value, maybe do something later?
            temp1 = temp1 + player_info[2]
            already_picked.append(index)
            #print(teams)
            

            
        elif (temp2 <= balanced or temp2 <= kinda_bal) and len(teams["Team2"]) < 5 and index not in already_picked:

            teams["Team2"].extend([player_info[1]])
            Ranks["Team2"].extend([player_info[0]])
            team2 = team2 + player_info[2]
            temp2 = temp2 + player_info[2]
            already_picked.append(index)
            #print(teams)
        

        elif (temp3 <= balanced or temp3 <= kinda_bal) and len(teams["Team3"]) < 5 and index not in already_picked:

  
            teams["Team3"].extend([player_info[1]])
            Ranks["Team3"].extend([player_info[0]])

            team3 = team3 + player_info[2]
            temp3 = temp3 + player_info[2]
            already_picked.append(index)
            #print(teams)
            



            
        elif (temp4 <= balanced or temp4 <= kinda_bal) and len(teams["Team4"]) < 5 and index not in already_picked:

            teams["Team4"].extend([player_info[1]])
            Ranks["Team4"].extend([player_info[0]])
            team4 = team4 + player_info[2]
            temp4 = temp4 + player_info[2]
            already_picked.append(index)
            #print(teams)
        
        
            


            
        elif (temp5 <= balanced or temp5 <= kinda_bal) and len(teams["Team5"]) < 5 and index not in already_picked:


            teams["Team5"].extend([player_info[1]])
            Ranks["Team5"].extend([player_info[0]])
            team5 = team5 + player_info[2]
            temp5 = temp5 + player_info[2]
            already_picked.append(index)
            #print(teams)




        elif (temp6 <= balanced or temp6 <= kinda_bal) and len(teams["Team6"]) < 5 and index not in already_picked:
        
            teams["Team6"].extend([player_info[1]])
            Ranks["Team6"].extend([player_info[0]])
            team6 = team6 + player_info[2]
            temp6 = temp6 + player_info[2]#we subtract regardless, so add twice so it remains a true value
            already_picked.append(index)
            #print(teams)

        elif (temp7 <= balanced or temp7 <= kinda_bal) and len(teams["Team7"]) < 5 and index not in already_picked:


            teams["Team7"].extend([player_info[1]])
            Ranks["Team7"].extend([player_info[0]])
            team7 = team7 + player_info[2]
            temp7 = temp7 + player_info[2]
            already_picked.append(index)
            #print(teams)

        elif (temp8 <= balanced or temp8 <= kinda_bal) and len(teams["Team8"]) < 5 and index not in already_picked:


            teams["Team8"].extend([player_info[1]])
            Ranks["Team8"].extend([player_info[0]])
            team8 = team8 + player_info[2]
            temp8 = temp8 + player_info[2]
            already_picked.append(index)
            #print(teams)


    
        counts = counts + 1#count the loop

        temp1 = temp1 - player_info[2]
        temp2 = temp2 - player_info[2]
        temp3 = temp3 - player_info[2]
        temp4 = temp4 - player_info[2] 
        temp5 = temp5 - player_info[2]
        temp6 = temp6 - player_info[2]
        temp7 = temp7 - player_info[2]
        temp8 = temp8 - player_info[2]
    
        #print("Coutns: ", counts)
        #print(already_picked)
        
        if counts == 10_000:#give the loop 10k tries, if it cant compute result from then, then restart
            '''print("#########################################FAILED ATTEMPT##############################################################")
            print("This is len of already: ",len(already_picked))
            print(teams)'''
           
            return None, None
        

        if len(teams["Team1"]) == len(teams["Team2"]) == len(teams["Team3"]) == len(teams["Team4"]) == len(teams["Team5"]) == len(teams["Team6"]) == len(teams["Team7"]) ==len(teams["Team8"]) == 5: #If teams are formed break
            print("###########################################SUCESS ATTEMPT############################################################")
            print("IDEAL POINTS PER TEAM: ", balanced)
            print("This is team1 Points: ", team1)
            print("This is team2 Points: ", team2)
            print("This is team3 Points: ", team3)
            print("This is team4 Points: ", team4)
            print("This is team5 Points: ", team5)
            print("This is team6 Points: ", team6)
            print("This is team7 Points: ", team7)
            print("This is team8 Points: ", team8)
            #print(teams)
            print(Ranks)

            final_teams = pd.DataFrame.from_dict(teams)
            print(final_teams.head(10))
            

            
            return teams, Ranks
    


    return None, None


trys = 0
x = None# result
y = None
while trys <= 10000:#x == None or y == None: #if result is still none keep trying

    
    x , y = weighted_sort(df)


    trys = trys +1
    #print("__________________________________________________________________________________________________________________________________",trys)

