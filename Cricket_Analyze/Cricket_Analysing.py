import plotly.express as px
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from Functions import *
from streamlit_option_menu import option_menu
import plotly.graph_objects as go


# -------------------------------- Page Title --------------------------------------------
st.set_page_config(page_title = 'Cricket Analyze')

# -------------------------------- Add BackGround image  --------------------------------------------
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://st2.depositphotos.com/1001941/6345/v/600/depositphotos_63452319-stock-illustration-cricket-sports-concept-with-red.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 
# -------------------------------- lottie bird animation -------------------------------------------- 

st.markdown("<h1 style='text-align: center; color: Black;'>Cricket Analyze</h1>", unsafe_allow_html=True)

def load_lottieURl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_bird = load_lottieURl("https://assets8.lottiefiles.com/packages/lf20_Hw1OgduFe1.json")

st_lottie(lottie_bird, height=300, width=700, key='bird')

# -------------------------------- Streamlit Setups -------------------------------------------- 


#--------------------------------------------  ----------------------------------------------

#1st innings
df_innings1 = Team1()
batsmen_df_in1, extras_df_in1, total_df_in1, bowlers_df_in1 = innings1(df_innings1)

# 2nd innings
df_innings2 = Team2()
batsmen_df_in2, extras_df_in2, total_df_in2, bowlers_df_in2 = innings2(df_innings2)

#------------------------------------------------------------------------------------
menu = option_menu(
                    menu_title='Cricket Analyze',
                    options=['Live Score',
                            'Team Scorecard',
                            'Analysis'],
                    icons=['activity', 'back',
                            'back', 'pie-chart'],
                    default_index=0,
                    orientation = "horizontal")

if menu == 'Live Score':
    #scrape = st.button("Cricket - LIVE SCORE")

    url = 'https://www.cricbuzz.com/'

    def livescore(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        live_scores = soup.find_all('div', {'class': 'cb-lv-scrs-col text-black'})

        score_list = []
        for score in live_scores:
            if 'IND' in score.text or 'AUS' in score.text:
                score_list.append(score.text.strip())

        df = pd.DataFrame(score_list, columns=['Live Scores'])
        return df

    df_livescore = livescore(url)
    st.dataframe(df_livescore)


if menu == 'Team Scorecard':
    Teams = ["IND","AUS"]
    Team_Selection = st.selectbox('Select the Team:', options= Teams)

    if Team_Selection == 'IND':
    
        st.markdown(
            """
            <button class="button-with-logo">
                <img src="https://img.etimg.com/thumb/msid-59202287,width-300,height-225,imgsize-66221,,resizemode-75/.jpg" alt="Logo" width="500" height="250">  
            </button>
            """
            , unsafe_allow_html=True
        )

        st.dataframe(batsmen_df_in1)
        st.dataframe(extras_df_in1)
        st.dataframe(total_df_in1)
        st.dataframe(bowlers_df_in1)

    if Team_Selection == 'AUS':
         
         st.markdown(
            """
            <button class="button-with-logo">
                <img src="https://static.toiimg.com/thumb/msid-80477273,imgsize-26736,width-400,resizemode-4/80477273.jpg" alt="Logo" width="500" height="250">  
            </button>
            """
            , unsafe_allow_html=True)

         st.dataframe(batsmen_df_in2)
         st.dataframe(extras_df_in2)
         st.dataframe(total_df_in2)
         st.dataframe(bowlers_df_in2)

if menu == 'Analysis':
            
        Teams = ["IND","AUS"]

        Team_Selection = st.selectbox('Select the Team:', options= Teams)

        if Team_Selection == "IND":

            Analyze = ["Top 5 Run Scorer",
                       "Top 5 Wicket Taker",
                       "Top Bowling Analyze",
                       "Team Strike Rate Analyze"]
            
            Analyze_Selection = st.selectbox('Select the Team:', options= Analyze)

            Runs_1 = batsmen_df_in1.sort_values('Runs',ascending = False).head()
            Runs_1 = Runs_1.sort_values('Runs')
            Bowl_1 = bowlers_df_in2.sort_values('W',ascending = False).head()
            ECO_1 = bowlers_df_in2.sort_values(['W','ECO'],ascending = [False,True])

            if Analyze_Selection == "Top 5 Run Scorer":

                # Create a scatter plot of the number of balls vs. run rate
                bar_trace = go.Bar(x=Runs_1["Batsman"], y=Runs_1["Runs"])
                line_trace = go.Scatter(x=Runs_1["Batsman"], y=Runs_1["Runs"],line=dict(color='orange'), yaxis='y2')

                layout = go.Layout(
                    title='Bar and Line Chart with Dual Axis',
                    yaxis=dict(title='Bar Data'),
                    yaxis2=dict(title='Line Data', overlaying='y', side='right')
                )

                fig = go.Figure(data=[bar_trace, line_trace], layout=layout)
                st.plotly_chart(fig)

            if Analyze_Selection == "Top 5 Wicket Taker":

                # Create a scatter plot of the number of balls vs. run rate
                fig = px.bar(
                    Bowl_1,
                    x='Bowler',
                    y='W',
                    title='Bowling Analyze',
                    hover_data=['W','ECO','Bowler']
                )
                st.plotly_chart(fig)

            if Analyze_Selection == "Top Bowling Analyze":

                # Create a scatter plot of the number of balls vs. run rate
                fig = px.bar(
                    ECO_1,
                    x='Bowler',
                    y='ECO',
                    title='Bowling Analyze',
                    hover_data=['W','ECO','Bowler']
                )
                st.plotly_chart(fig)

            if Analyze_Selection == "Team Strike Rate Analyze":

                fig = go.Figure(go.Scatter(x = batsmen_df_in1['Batsman'],
                                           y = batsmen_df_in1['SR'],
                                           line=dict(color='blue'),
                                           marker=dict(color='orange'),
                                           mode = 'lines+markers'))
                st.plotly_chart(fig)

            #-----------------------------------------------------------------#

        if Team_Selection == "AUS":

            Analyze = ["Top 5 Run Scorer",
                       "Top 5 Wicket Taker",
                       "Top Bowling Analyze",
                       "Team Strike Rate Analyze"]
            
            Analyze_Selection = st.selectbox('Select the Team:', options= Analyze)

            Runs_2 = batsmen_df_in2.sort_values('Runs',ascending = False).head()
            Bowl_2 = bowlers_df_in1.sort_values('W',ascending = False).head()
            ECO_2 = bowlers_df_in1.sort_values(['W','ECO'],ascending = [False,True])

            if Analyze_Selection == "Top 5 Run Scorer":

                # Create a scatter plot of the number of balls vs. run rate
                bar_trace = go.Bar(x=Runs_2["Batsman"], y=Runs_2["Runs"], marker=dict(color='yellow'))
                line_trace = go.Scatter(x=Runs_2["Batsman"], y=Runs_2["Runs"],line=dict(color='green'), yaxis='y2')

                layout = go.Layout(
                    title='Bar and Line Chart with Dual Axis',
                    yaxis=dict(title='Bar Data'),
                    yaxis2=dict(title='Line Data', overlaying='y', side='right')
                )

                fig = go.Figure(data=[bar_trace, line_trace], layout=layout)
                st.plotly_chart(fig)



    
            if Analyze_Selection == "Top 5 Wicket Taker":

                # Create a scatter plot of the number of balls vs. run rate
                fig = px.bar(
                    Bowl_2,
                    x='Bowler',
                    y='W', 
                    color_discrete_sequence=['yellow'],
                    title='Bowling Analyze',
                    hover_data=['W','ECO','Bowler']
                )
                st.plotly_chart(fig)

            if Analyze_Selection == "Top Bowling Analyze":

                # Create a scatter plot of the number of balls vs. run rate
                fig = px.bar(
                    ECO_2,
                    x='Bowler',
                    y='ECO',
                    color_discrete_sequence=['yellow'],
                    title='Bowling Analyze',
                    hover_data=['W','ECO','Bowler']
                )
                st.plotly_chart(fig)
                
            if Analyze_Selection == "Team Strike Rate Analyze":

                fig = go.Figure(go.Scatter(x = batsmen_df_in2['Batsman'],
                                           y = batsmen_df_in2['SR'],
                                           line=dict(color='yellow'),
                                           marker=dict(color='green') ,
                                           mode = 'lines+markers'))
                st.plotly_chart(fig)
            

              