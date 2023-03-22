import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import warnings


# --------------------------- Innings 1 data -----------------------------------

def Team1():
        url = "https://www.cricbuzz.com/live-cricket-scorecard/56208/rsa-vs-wi-3rd-odi-west-indies-tour-of-south-africa-2023"
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
        
        return pd.read_csv("scorecard_innings1.csv")



def innings1(df_innings1):
            extras_index = df_innings1.index[df_innings1['Batsman'] == 'Extras'][0]
            batsmen_df_in1 = df_innings1.loc[:extras_index-1].reset_index(drop=True)
            batsmen_df_in1.index = batsmen_df_in1.index + 1
            # Data Cleaning
            batsmen_df_in1.dropna(how = "all",axis = 1, inplace = True)
            batsmen_df_in1['Runs'] = batsmen_df_in1.Runs.apply(lambda x: int(x))


            # Group data by extras
            extras_index = df_innings1.index[df_innings1['Batsman'] == 'Extras'][0]
            extras_df_in1 = df_innings1.iloc[extras_index: extras_index+1].reset_index(drop=True)
            extras_df_in1 = extras_df_in1.rename(columns={"Batsman": "Extras",'Dismissal':'Extra Runs'})
            extras_df_in1.dropna(how = "all",axis = 1, inplace = True)
            
            # Group data by total
            extras_index = df_innings1.index[df_innings1['Batsman'] == 'Extras'][0]
            total_df_in1 = df_innings1.iloc[extras_index+1:extras_index+2].reset_index(drop=True)

            total_df_in1 = total_df_in1.rename(columns={"Batsman": "Totals",'Dismissal':'Total Runs'})
            total_df_in1.index = total_df_in1.index+1
            total_df_in1.dropna(how = "all",axis = 1, inplace = True)

            # Group data by bowlers
            extras_index = df_innings1.index[df_innings1['Batsman'] == 'Extras'][0]
            bowlers_df_in1 = df_innings1.iloc[extras_index+3: ].reset_index(drop=True)
            bowlers_df_in1 = bowlers_df_in1.rename(columns={"Batsman": "Bowler",'Dismissal':'O','Runs':'M',"Balls":"R","4s":"W","6s":"NB","SR":"WD","Unnamed: 7":"ECO"})
            bowlers_df_in1.index = bowlers_df_in1.index+1
            bowlers_df_in1.dropna(how = "all",axis = 1, inplace = True)
            
            return batsmen_df_in1,extras_df_in1,total_df_in1,bowlers_df_in1

# --------------------------- Innings 2 data -----------------------------------

def Team2():
        url = "https://www.cricbuzz.com/live-cricket-scorecard/56208/rsa-vs-wi-3rd-odi-west-indies-tour-of-south-africa-2023"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        scorecard_table = soup.find("div", {"id": "innings_2"})
        if scorecard_table:
            rows = scorecard_table.find_all("div", {"class": "cb-col cb-col-100 cb-scrd-itms"})
            
            with open('scorecard_innings2.csv', 'w', newline='') as csvfile:
            
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

            print("CSV file for innings 2 created successfully.")
        
        return pd.read_csv("scorecard_innings2.csv")


                
def innings2(df_innings2):
    extras_index = df_innings2.index[df_innings2['Batsman'] == 'Extras'][0] if 'Extras' in df_innings2['Batsman'].values else -1
    if extras_index != -1:
        batsmen_df_in2 = df_innings2.loc[:extras_index-1].reset_index(drop=True)
        batsmen_df_in2.index = batsmen_df_in2.index + 1
        # Data Cleaning
        batsmen_df_in2.dropna(how="all", axis=1, inplace=True)
        batsmen_df_in2['Runs'] = batsmen_df_in2.Runs.apply(lambda x: int(x))

        # Group data by extras
        extras_df_in2 = df_innings2.iloc[extras_index:extras_index+1].reset_index(drop=True)
        extras_df_in2 = extras_df_in2.rename(columns={"Batsman": "Extras", 'Dismissal': 'Extra Runs'})
        extras_df_in2.index = extras_df_in2.index + 1
        extras_df_in2.dropna(how="all", axis=1, inplace=True)

        # Group data by total
        total_df_in2 = df_innings2.iloc[extras_index+1:extras_index+2].reset_index(drop=True)
        total_df_in2 = total_df_in2.rename(columns={"Batsman": "Totals", 'Dismissal': 'Total Runs'})
        total_df_in2.index = total_df_in2.index + 1
        total_df_in2.dropna(how="all", axis=1, inplace=True)

        # Group data by bowlers
        bowlers_df_in2 = df_innings2.iloc[extras_index+3:].reset_index(drop=True)
        bowlers_df_in2 = bowlers_df_in2.rename(columns={"Batsman": "Bowler", 'Dismissal': 'O', 'Runs': 'M', "Balls": "R", "4s": "W", "6s": "NB", "SR": "WD", "Unnamed: 7": "ECO"})
        bowlers_df_in2.index = bowlers_df_in2.index + 1
        bowlers_df_in2.dropna(how="all", axis=1, inplace=True)

        return batsmen_df_in2, extras_df_in2, total_df_in2, bowlers_df_in2
    else:
        return None, None, None, None

