import time
import csv
import sys 
import os
import numpy as np
import math
import matplotlib.pyplot as plt

def inversion(x):
	return 1-x

def l_average(trait_list,l):
	sum = 0
	for i in range(l-1,len(trait_list)):
		sum += trait_list[i]
	return sum/(len(trait_list)+1-l)

def l_std(trait_list,l,mean):
	sum = 0
	for i in range(l-1,len(trait_list)):
		sum += (trait_list[i] - mean)**2
	averaged_sum = sum/(len(trait_list)-l)
	return math.sqrt(averaged_sum)

def get_average(trait_list):
	average = 0
	for i in range(len(trait_list)):
		average += float(trait_list[i])
	return average/len(trait_list)

team_names = ["1-fc-koeln","borussia-dortmund","fc-schalke-04","borussia-moenchengladbach","fortuna-duesseldorf","sc-paderborn-07",
"tsg-1899-hoffenheim","1-fc-union-berlin","eintracht-frankfurt","1-fsv-mainz-05","fc-augsburg","hertha-bsc","sport-club-freiburg",
"vfl-wolfsburg","bayer-04-leverkusen","fc-bayern-muenchen","rb-leipzig","sv-werder-bremen"]

for team_name in team_names:

	with open(team_name + ".csv") as csv_file:
    		csv_reader = csv.reader(csv_file, delimiter=',')
    		d_ap = []
    		d_ir = []
    		d_s = []
    		N_ap = []
    		#number of matches dominated by the team itself
    		N_dm = 0
    		#number of countered dominations
    		N_cd = 0
    		row_count = 0
    		for row in csv_reader:
    			if row_count != 0:
    				d_ap.append(inversion(np.exp((-float(row[33]) + float(row[27]))/100)))
    				d_ir.append(np.exp(-float(row[27])))
    				d_s.append(np.exp(-float(row[28])))
    				N_ap.append(inversion(np.exp(-float(row[18])/float(row[19]))))
    				f_pp = float(row[23])
    				if f_pp > 65.0:
    					N_dm += 1
    				if f_pp < (100.0 - 65.0) and float(row[0]) > float(row[1]):
    					N_cd += 1
    			row_count += 1
		csv_file.close()

	num_of_matches = float(row_count-1)
	average_d_ap = get_average(d_ap)
	average_d_ir = get_average(d_ir)
	average_d_s = get_average(d_s)
	average_N_ap = get_average(N_ap)
	f_dm = N_dm/num_of_matches
	f_cd = inversion(N_cd/num_of_matches)
	strategy_score = 3.0/20 * (average_d_ap + average_d_ir) + 3.0/10 * (average_d_s + average_N_ap) + 1.0/20 * (f_dm + f_cd)
	
	d_ap_rob = []
	d_ir_rob = []
	d_s_rob = []
	N_ap_rob = []
	for l in range(1,len(d_ir)):
		d_ap_mean = l_average(d_ap,l)
		d_ap_std = l_std(d_ap,l,d_ap_mean)
		d_ap_index = d_ap_std/d_ap_mean
		d_ap_rob.append(np.exp(-d_ap_index))
		d_ir_mean = l_average(d_ir,l)
		d_ir_std = l_std(d_ir,l,d_ir_mean)
		d_ir_index = d_ir_std/d_ir_mean
		d_ir_rob.append(np.exp(-d_ir_index))
		d_s_mean = l_average(d_s,l)
		d_s_std = l_std(d_s,l,d_s_mean)
		d_s_index = d_s_std/d_s_mean
		d_s_rob.append(np.exp(-d_s_index))
		N_ap_mean = l_average(N_ap,l)
		N_ap_std = l_std(N_ap,l,N_ap_mean)
		N_ap_index = N_ap_std/N_ap_mean
		N_ap_rob.append(np.exp(-N_ap_index))
	f = plt.figure()
	plt.subplot(221)
	plt.title("Robsustness of d_ap")
	plt.plot(range(1,len(d_ap_rob)+1),d_ap_rob)
	plt.subplot(222)
	plt.title("Robsustness of d_ir")
	plt.plot(range(1,len(d_ir_rob)+1),d_ir_rob)
	plt.subplot(223)
	plt.title("Robsustness of d_s")
	plt.plot(range(1,len(d_s_rob)+1),d_s_rob)
	plt.subplot(224)
	plt.title("Robsustness of N_ap")
	plt.plot(range(1,len(N_ap_rob)+1),N_ap_rob)
	plt.subplots_adjust(hspace = 0.5)
	f.savefig(team_name + ".pdf")
	plt.close()

	file_name = team_name + "_vars_and_measures.csv"
	with open(file_name, mode="w") as team_file:
			writer = csv.writer(team_file, delimiter=",")
			writer.writerow(["d_apr","d_ir","d_s","N_ap","f_dm","f_cd","ss"])
			writer.writerow([average_d_ap,average_d_ir,average_d_s,average_N_ap,f_dm,f_cd,strategy_score])
			team_file.close()

