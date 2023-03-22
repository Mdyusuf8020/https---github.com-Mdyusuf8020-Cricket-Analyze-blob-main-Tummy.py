import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# --------------------------- Innings 1 data -----------------------------------

def Team1():
        url = "https://www.cricbuzz.com/live-cricket-scorecard/60037/ind-vs-aus-2nd-odi-australia-tour-of-india-2023"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        scorecard_table = soup.find("div", {"id": "innings_1"})
        if scorecard_table:
            rows = scorecard_table.find_all("div", {"class": "cb-col cb-col-100 cb-scrd-itms"})
            
            with open('scorecard_innings1.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write the header row
                writer.writerow(['Batsman', 'Dismissal', 'Runs', 'Balls', '4s', '6s', 'SR',''])

                # Write the data rows
                for row in rows:
                    cells = row.find_all("div", {"class": "cb-col"})
                    row_data = []
                    for cell in cells:
                        row_data.append(cell.text.strip())
                    writer.writerow(row_data)

            print("CSV file for innings 1 created successfully.")
        else:
            print("Scorecard table not found on the page.")
        return pd.read_csv("scorecard_innings1.csv")



def innings1(df_innings1):
            batsmen_df_in1 = df_innings1.iloc[0:11]
            batsmen_df_in1.index = batsmen_df_in1.index + 1
            # Data Cleaning
            batsmen_df_in1.dropna(how = "all",axis = 1, inplace = True)
            batsmen_df_in1['Runs'] = batsmen_df_in1.Runs.apply(lambda x: int(x))


            # Group data by extras
            extras_df_in1 = df_innings1.iloc[11:12].rename(columns={"Batsman": "Extras",'Dismissal':'Extra Runs'})
            extras_df_in1.index = extras_df_in1.index+1
            extras_df_in1.dropna(how = "all",axis = 1, inplace = True)
            
            # Group data by total
            total_df_in1 = df_innings1.iloc[12:13].rename(columns={"Batsman": "Totals",'Dismissal':'Total Runs'})
            total_df_in1.index = total_df_in1.index+1
            total_df_in1.dropna(how = "all",axis = 1, inplace = True)

            # Group data by bowlers
            bowlers_df_in1 = df_innings1.iloc[13:].rename(columns={"Batsman": "Bowler",'Dismissal':'O','Runs':'M',"Balls":"R","4s":"W","6s":"NB","SR":"WD","Unnamed: 7":"ECO"})
            bowlers_df_in1.index = bowlers_df_in1.index+1
            bowlers_df_in1.dropna(how = "all",axis = 1, inplace = True)
            
            return batsmen_df_in1,extras_df_in1,total_df_in1,bowlers_df_in1

# --------------------------- Innings 2 data -----------------------------------

def Team2():

        url = "https://www.cricbuzz.com/live-cricket-scorecard/60037/ind-vs-aus-2nd-odi-australia-tour-of-india-2023"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        with open('scorecard_innings2.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row
            writer.writerow(['Batsman', 'Dismissal', 'Runs', 'Balls', '4s', '6s', 'SR', ''])
            # Write the data rows
            for innings in range(2,3):
                scorecard_table = soup.find("div", {"id": "innings_" + str(innings)})
                rows = scorecard_table.find_all("div", {"class": "cb-col cb-col-100 cb-scrd-itms"})
                
            # Write the data rows
            for row in rows:
                cells = row.find_all("div", {"class": "cb-col"})
                row_data = []
                for cell in cells:
                    row_data.append(cell.text.strip())
                writer.writerow(row_data)
        return pd.read_csv("scorecard_innings2.csv")  
                

def innings2(df_innings2):
    batsmen_df_in2 = df_innings2.iloc[0:2]
    batsmen_df_in2.index = batsmen_df_in2.index+1
    batsmen_df_in2.dropna(how = "all",axis = 1, inplace = True)
    batsmen_df_in2['Runs'] = batsmen_df_in2.Runs.apply(lambda x: int(x))

    
    
    # Group data by extras
    extras_df_in2 = df_innings2.iloc[2:3].rename(columns={"Batsman": "Extras",'Dismissal':'Extra Runs'})
    extras_df_in2.index = extras_df_in2.index+1
    extras_df_in2.dropna(how = "all",axis = 1, inplace = True)

    # Group data by total
    total_df_in2 = df_innings2.iloc[3:4].rename(columns={"Batsman": "Totals",'Dismissal':'Total Runs'})
    total_df_in2.index =total_df_in2.index+1
    total_df_in2.dropna(how = "all",axis = 1, inplace = True)

    # Group data by bowlers
    bowlers_df_in2 = df_innings2.iloc[5:].rename(columns={"Batsman": "Bowler",'Dismissal':'O','Runs':'M',"Balls":"R","4s":"W","6s":"NB","SR":"WD","Unnamed: 7":"ECO"})
    bowlers_df_in2.index =bowlers_df_in2.index+1
    bowlers_df_in2.dropna(how = "all",axis = 1, inplace = True)

    
    return batsmen_df_in2,extras_df_in2,total_df_in2,bowlers_df_in2
    
