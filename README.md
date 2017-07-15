# IPL-score-prediction
A Big Data Analytics project which focused on the prediction of a team score given the players in the team with their batting order.Comparing the scores of the teams ,a winner is  chosen

Used the IPL match data from season3-season9 and calculated the probabilities of a batsman scoring different scores,
from 0 to 6 .Also the player statstics was scaped from cricketarchive.com and was used for clustering.
clustering was done using an infrastructure called Spark specifically SparkML libraries.
For the batsmen who never faced a bowler,the cluster information was used to calculate the probabilities.
Finally a match simulator was written in python which expected the player order of both teams as input and would produce the scores of each team.Based on the scores a winner is determined.
