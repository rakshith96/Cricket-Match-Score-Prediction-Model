import xlrd
import glob
import pandas as pd
import csv
import xlwt
from player_info import player_name_clust_map,cluster_info,player_name_mapping
from collections import defaultdict
from pprint import pprint
import math
import os
import sys

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
bowler_cluster_map=defaultdict(lambda:-1)
not_added=list()


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
		
		bowler_cluster=''
		batsman_cluster=''
		
		flag=0
		
		for key,value in player_name_clust_map.iteritems():
			if key ==current_bat:
				batsman_cluster=value[1]
				#print(current_bat,batsman_cluster)
				break
				
		for key,value in player_name_mapping.iteritems():
			if key ==current_bowl:
				flag=1
				current_bowl=value
				#print(current_bowl)
				break
				
							
		#print(bowler_cluster_map.keys())		
		if(current_bowl not in bowler_cluster_map.keys()):			
			if(flag==1):		
				f=open("/home/supg/Desktop/BowlerClusterData.csv")
			
				for every_line in f.readlines():
					if(current_bowl in every_line.strip().split(',')[0]):
						#print(every_line.split(',')[4])
						bowler_cluster_map[current_bowl]=int(every_line.split(',')[4][0])
						#print(every_line.split(',')[0],current_bowl,bowler_cluster_map[current_bowl])
						break
				f.close()
		#else:print("hello"+current_bowl)
		
		if(flag == 0):
			#print(current_bowl)
			if(current_bowl not in not_added):
				not_added.append(current_bowl)
		
		bowler_cluster=bowler_cluster_map[current_bowl]
		#if(bowler_cluster_map[current_bowl] == -1):print(current_bowl)
		#print(current_bowl,bowler_cluster)
				

		
		if(current_out != ''):
			type_of_run[7][batsman_cluster][bowler_cluster]+=1
			#print(batsman_cluster,bowler_cluster,type_of_run[7][batsman_cluster][bowler_cluster])
			continue
		else:
			type_of_run[current_run][batsman_cluster][bowler_cluster]+=1
			#print(batsman_cluster,bowler_cluster,type_of_run[current_run][batsman_cluster][bowler_cluster])
		if(current_extra != 0):
			type_of_run[8][batsman_cluster][bowler_cluster]+=1
			#print(batsman_cluster,bowler_cluster,type_of_run[8][batsman_cluster][bowler_cluster])
'''	
for every_key in bowler_cluster_map:	
	if(bowler_cluster_map[every_key]==-1):
		print(every_key)
'''
#pprint(bowler_cluster_map)


#print(not_added)

#sys.stdout=open('cluster_vs_cluster.csv','w')
file_write=open('cluster_vs_cluster.csv','w')

file_write.write('Batsman_cluster'+","+'Bowler_cluster'+","+'0s_prob'+","+'1s_prob'+","+'2s_prob'+","+'3s_prob'+","+'4s_prob'+","+'5s_prob'+","+'6s_prob'+","+'outs_prob'+","+'extras_prob'+"\n")
for i in range(0,10):
	for j in range(0,10):
		list_of_count=list()
		for every_run in range(0,9):
			list_of_count.append(type_of_run[every_run][i][j])
		total=sum(list_of_count)
		#print(list_of_count,total)
		if(total == 0):total=1
		prob=list(map(lambda x: x/float(total),list_of_count))
		file_write.write(str(i)+","+str(j)+","+str(prob[0])+","+str(prob[1])+","+str(prob[2])+","+str(prob[3])+","+str(prob[4])+","+str(prob[5])+","+str(prob[6])+","+str(prob[7])+","+str(prob[8])+"\n");
		#for every_run in range(0,9):
			#print(list_of_count[every_run]/total)
		
