# -*- coding: utf-8 -*-
"""ipl_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gb5ONjRr3AtRoRVZYlHDeFobVEa0RpAG

to import libraries
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""to read match data"""

match_data=pd.read_csv("/content/sample_data/ipl_match_info_data.csv")
match_data.head()

"""to read ball data"""

ball_data=pd.read_csv("/content/sample_data/ipl_match_ball_by_ball_data.csv")
ball_data.head()

"""to find null values in each column"""

match_data.isnull().sum()

ball_data.isnull().sum()

"""to find shape of match and ball dataset"""

match_data.shape

ball_data.shape

match_data.columns

ball_data.shape

ball_data.columns

"""to find the total number of matches played so far"""

print("matches played so far:",match_data.shape[0])
print("/n cities:",match_data["city"].unique())
print("/n teams:",match_data["team1"].unique())

"""to retrive year from date"""

match_data['season']=pd.DatetimeIndex(match_data['date']).year
print(match_data['season'].unique())

"""number of matches per season"""

matches_per_season = match_data.groupby("season")["match_id"].count().reset_index().rename(columns={"match_id":"matches"})
matches_per_season

"""to plot bar graph of the number of matches per season"""

sns.countplot(x="season",data=match_data)
plt.xticks(rotation=45,fontsize=10)
plt.yticks(fontsize=10)
plt.xlabel("season")
plt.ylabel("number of matches")
plt.title("number of matches per season",fontweight="bold")

season_data=match_data[["match_id","season"]].merge(ball_data,left_on="match_id",right_on="match_id",how="left").drop("match_id",axis=1)
season_data.head()

ball_data.columns

season_data["total_runs"]=season_data[["runs_off_bat","extras"]].sum(axis=1)
season_data.tail()

"""to plot runs scored in each season"""

season=season_data.groupby("season_x")["total_runs"].sum().reset_index()
p=season.set_index("season_x")
sns.lineplot(data=p,palette="magma")
plt.xlabel("season")
plt.ylabel("runs")
plt.title("total runs scored each season",fontweight="bold")

runs_per_season=pd.concat([matches_per_season,season.iloc[:,1]],axis=1)
runs_per_season["runs_per_match"] =runs_per_season["total_runs"]/runs_per_season["matches"]  
runs_per_season.set_index("season",inplace=True)         
runs_per_season

toss=match_data["toss_winner"].value_counts()
sns.barplot(y=toss.index,x=toss,palette="icefire",saturation=1)
plt.ylabel("teams")
plt.xlabel("no. of tosses won")
plt.title("number of tosses won by each team",fontweight="bold")

sns.countplot(x="season",hue="toss_decision",data=match_data,palette="magma",saturation=1)
plt.xticks(rotation=90)
plt.xlabel("season")
plt.title("toss decisions",fontweight="bold")

match_data["result_type"].value_counts()

match_data.venue[match_data.result_type!="chased"].mode()
match_data.venue[match_data.result_type!="defended"].mode()

"""best stadium for defending"""

best_for_defending=match_data["venue"][match_data["result_type"]!="chased"].mode()
best_for_defending

"""best stadium for chasing"""

best_for_chasing=match_data["venue"][match_data["result_type"]!="defended"].mode()
best_for_chasing

"""best stadium to win the toss"""

match_data["venue"][match_data["toss_winner"]=="Chennai Super Kings"][match_data["winner"]=="Chennai Super Kings"].mode()

"""for Mumbai indians using different syntax"""

match_data.venue[match_data.toss_winner=="Mumbai Indians"][match_data.winner=="Mumbai Indians"].mode()

"""best chasing team"""

match_data.winner[match_data.result_type=="chased"].mode()

"""best definding team"""

match_data.winner[match_data.result_type=="defended"].mode()

"""does winning toss means winning the match"""

sns.countplot(match_data.toss_winner == match_data.winner)

sns.countplot(match_data.toss_decision[match_data.winner==match_data.toss_winner])

player=(ball_data["striker"]=="V Kohli")
df_virat=ball_data[player]
df_virat.head()

df_virat["wicket_type"].value_counts().plot.pie(autopct="%1.1f%%",rotatelabels=True)
plt.title("dismissal types",fontweight="bold")

def count(df_virat,runs):
  return len(df_virat[df_virat["runs_off_bat"]==runs])*runs

print("runs scored from 1s: ",count(df_virat,1))
print("runs scored from 2s: ",count(df_virat,2))
print("runs scored from 3s: ",count(df_virat,3))
print("runs scored from 4s: ",count(df_virat,4))
print("runs scored from 6s: ",count(df_virat,6))

pd.set_option('display.max_columns', None)
match_data[match_data["winner_runs"]==match_data["winner_runs"].max()]

runs=ball_data.groupby(["striker"])["runs_off_bat"].sum().reset_index()
runs.columns=["batsman","runs"]
y=runs.sort_values(by="runs",ascending=False).head(10).reset_index().drop("index",axis=1)
y

sns.barplot(x=y["batsman"],y=y["runs"],palette="icefire",saturation=1)
plt.xticks(rotation=90,fontsize="10")
plt.title("top scorers")

wickets=ball_data.groupby(["bowler"])["wicket_type"].count().reset_index()
wickets.columns=["bowler","wickets"]
z=wickets.sort_values(by="wickets",ascending=False).head(10).reset_index().drop("index",axis=1)
z

best_player=match_data["player_of_match"].value_counts().head(10).reset_index()
best_player.columns=["player","player_of_match"]
best_player

sns.barplot(x=best_player["player"],y=best_player["player_of_match"])
plt.xticks(rotation=90,fontsize=10)
plt.title("best players",fontweight="bold")