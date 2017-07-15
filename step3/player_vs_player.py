import xlrd
import glob
import pandas as pd
import csv
import xlwt
from player_info import player_name_clust_map,cluster_info
from collections import defaultdict
from pprint import pprint
import math
import os

directory_path="/home/supg/Desktop/probabilities"
if not os.path.exists(directory_path):
	os.makedirs(directory_path)
os.chdir(directory_path)	
	
no_of_zeros=defaultdict(lambda:defaultdict(lambda:0))
no_of_ones=defaultdict(lambda:defaultdict(lambda:0))
no_of_twos=defaultdict(lambda:defaultdict(lambda:0))
no_of_threes=defaultdict(lambda:defaultdict(lambda:0))
no_of_fours=defaultdict(lambda:defaultdict(lambda:0))
no_of_fives=defaultdict(lambda:defaultdict(lambda:0))
no_of_sixes=defaultdict(lambda:defaultdict(lambda:0))
no_of_outs=defaultdict(lambda:defaultdict(lambda:0))
no_of_extras=defaultdict(lambda:defaultdict(lambda:0))


type_of_run=[no_of_zeros,no_of_ones,no_of_twos,no_of_threes,no_of_fours,no_of_fives,no_of_sixes,no_of_outs,no_of_extras]

list_of_all_matches=sorted(list(glob.glob("/home/supg/Desktop/Match_data/Match*")))

for every_match in list_of_all_matches:

	book = xlrd.open_workbook(every_match)
	sheet = book.sheet_by_index(0)
	rows = sheet.nrows
	
	for row in range(1, rows):
		current_bat=str(sheet.cell(row,0))[8:-1]
		#print(current_bat)
		current_bowl=str(sheet.cell(row,2))[8:-1]
		#print(current_bowl)
		current_run=int(str(sheet.cell(row,3))[-2])
		#print(current_run)
		current_extra=int(float((str(sheet.cell(row,4))[7:])))
		#print(current_extra)
		current_out=str(sheet.cell(row,5))
		if('empty' in current_out):current_out=''
		else:current_out=current_out[-3:]
		#print(current_out)
		
		
		if(current_out != ''):
			type_of_run[7][current_bat][current_bowl]+=1
			continue
		else:
			type_of_run[current_run][current_bat][current_bowl]+=1
			
		if(current_extra != 0):
			type_of_run[8][current_bat][current_bowl]+=1
#pprint(dict(type_of_run[4]))

#print(type_of_run[4]['F du Plessis']['A Nehra'])

batsman_name = sorted(list(pd.read_csv("/home/supg/Desktop/ipl_batsman_profiles.csv")["Name"]))
bowler_name = sorted(list(pd.read_csv("/home/supg/Desktop/ipl_bowler_profiles.csv")["Name"]))

for every_batsman in batsman_name:
	
	for key,value in player_name_clust_map.iteritems():
		if value[0] == every_batsman:
			every_batsman=key
			break
			#print(every_batsman)
			
	write_file=open(every_batsman+".csv",'w')
	fieldnames = ['Batsman','Bowler','0s_prob','1s_prob','2s_prob','3s_prob','4s_prob','5s_prob','6s_prob','outs_prob','extras_prob']
	csv_writer=csv.DictWriter(write_file,fieldnames=fieldnames)
	csv_writer.writeheader()
	
	for every_bowler in bowler_name:
		
		for key,value in player_name_clust_map.iteritems():
			if value[0] == every_bowler:
				every_bowler=key
				break
				
		if(every_batsman == every_bowler):
			continue
					
		for every_score in range(0,9):
			total_count=0
			avg_count=0
			if(type_of_run[every_score][every_batsman][every_bowler] == 0):
				try:	
					bat_cluster=player_name_clust_map[every_batsman][1]
				except KeyError:
					for key,value in cluster_info.iteritems():
						if every_batsman in value:
							bat_cluster=key
							break
					
				cluster_list=cluster_info[bat_cluster]
				for every_cluster_batsman in cluster_list:
					total_count+=type_of_run[every_score][every_cluster_batsman][every_bowler]
				#print(total_count,every_batsman,every_bowler)
				avg_count=math.ceil(total_count/len(cluster_list))
				type_of_run[every_score][every_batsman][every_bowler]=avg_count
				
				
		count_list=list()	
		for every_run in range(0,9):
			count_list.append(type_of_run[every_run][every_batsman][every_bowler])
		#print(count_list)
		length=sum(count_list)
		if(length == 0):length=1
		csv_writer.writerow({'Batsman':every_batsman,'Bowler':every_bowler,'0s_prob':count_list[0]/length,'1s_prob':count_list[1]/length,'2s_prob':count_list[2]/length,'3s_prob':count_list[3]/length,'4s_prob':count_list[4]/length,'5s_prob':count_list[5]/length,'6s_prob':count_list[6]/length,'outs_prob':count_list[7]/length,'extras_prob':count_list[8]/length});
		
	write_file.close()
		
				
"""
i=0
for every in type_of_run:
	print(i)
	for some in every:
		pprint(some)	
	i+=1
"""
