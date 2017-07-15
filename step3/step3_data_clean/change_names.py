import csv
import re
from collections import defaultdict
from pprint import pprint
import sys

name_change=defaultdict(lambda:0)
matches=list()
fbook_list=list()
f_profile_list=list()
f_profile_list_string=''

with open('/home/supg/Desktop/nname.csv','r') as fbook,open("/home/supg/Desktop/BatsmanClusterData.csv",'r') as f_profile:
	fbook_reader=csv.DictReader(fbook)
	f_profile_reader=csv.DictReader(f_profile)
	
	
	for row in fbook_reader: #read all the names which have appeared in the pvp data
		ll=row['names']
		if(ll == ' '):
			break
		else:fbook_list.append(ll)
		
	for row in f_profile_reader:	#read all the names of the player in batting profile 
		batsman=row['Batsman_name']
		if(batsman == ' '):
			break
		else:f_profile_list.append(batsman)
		
	#print(fbook_list)
		
	for every_ele in fbook_list:  		#for every name in pvp data
		match_list=list()
		for i in range(len(f_profile_list)):	#following code generates a list of matching names
			x=f_profile_list[i]
			#print(every_ele.split()[-1:][0])
			if every_ele.split()[-1:][0] in x:	#check for existance of last name in profile data entry
				#x=x.split()
				#print(x.rsplit(' ',1)[0][0:len(x)-1])
				#print(every_ele.split())
				#print(every_ele.rsplit(' ',1)[0])
				sll=every_ele.rsplit(' ',1)[0].split()	#get all the first n-2 words of name
				#print(sll)
		
				if(len(sll) >1):		#check if the length of those n-2  names is greater than 1
					length_list=list(map(len,sll))	#find the length of all those words
					sbb=sll[length_list.index(max(length_list))]#find max length word
				else:sbb=every_ele.split()[0][0]	#else the n-2 names is just a single word or a letter
				
				if(sbb.isupper()):	#if a single word and is an acronym for the first name
					sbb=sbb[0]	#get the first character
					#print(sbb)
					#print(list(map(lambda x:x[0],x.rsplit(' ',1)[0].split())))
					if sbb in list(map(lambda x:x[0],x.rsplit(' ',1)[0].split())):#check with all the first characters in the first name
						match_list.append(x) 
						
				#print(sbb)
				#print(x.rsplit(' ',1)[0][0:len(x)-1])
				elif(sbb in x.rsplit(' ',1)[0]):#search first word in first n-2 words
					#print(every_ele.split()[0][0])
					#print(x)
					match_list.append(x)#find all the matches
				
		if(len(match_list)==1):
			name_change[every_ele]=match_list[0]#if only one match select it
			print(every_ele+"="+match_list[0])
		elif len(match_list) >0 :
			#print(match_list)			#more than one match ->ask user to provide index of the right match
			print("'"+every_ele+"'  matches:")
			for i in range(0,len(match_list)):
				print(match_list[i]+" "+str(i),end=',')#display the possible matchings along with the indices for choosing
			print()
			print("are there any matches?")
			ch=input("y/n \n")
			if(ch == 'y'):	#if true then get the match
				index=int(input())#enter the index in terminal
				name_change[every_ele]=match_list[index]
				print(every_ele+"="+match_list[index])
				continue
			else:print("element "+every_ele+"not matched by user")#else assign 0
	
	output_file_name="player_mapping10.py"
	sys.stdout=open(output_file_name,'w')
	#print("player_name_mapping={")
	print("player_name_mapping=")
	#pprint(name_change)#dump all the mappings into a file.
	pprint(dict(name_change))#dump all the mappings into a file.
	#print("}")


'''
#include this for double check code in player_mapping file.
found three players missing
L Ablish
S Anirudha
S Vidyut

print(len(player_name_mapping))
import csv
fbook=open('/home/supg/Desktop/nname.csv','r')
fbook_reader=csv.DictReader(fbook)
for row in fbook_reader: 
		ll=row['names']
		all_names=player_name_mapping.keys()
		if ll not in all_names:
			print(ll)
'''	
