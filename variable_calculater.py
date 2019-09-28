import time
import csv
import sys 
import os
import numpy as np
import math
import matplotlib.pyplot as plt

def inversion(x):
	return 1-x

def g(x):
	alpha = 1.0
	return (np.exp(alpha*x)-1)/(np.exp(alpha)-1)

def normalization(x,scale):
	#return np.exp(-x/scale)
	return 1 - 2/math.pi * np.arctan(x/scale)
	#return 1/(1+x/scale)

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

def get_population_std(average,trait_list):
	std = 0
	for trait in trait_list:
		std += (average - trait)**2
	return math.sqrt(std/float(len(trait_list)))


def l_sum(trait_list,lower):
	s = 0
	for i in range(lower,len(trait_list)):
		s += trait_list[i]
	return s

def mu_ss(d_apr,d_ir,d_s,N_ap,f_dm,f_cd):
	strategy_score = 3.0/20 * (g(N_ap) + g(d_ir)) + 3.0/10 * (g(d_s) + g(d_apr)) + 1.0/20 * (g(f_dm) + g(f_cd))
	return strategy_score


team_names = ["1-fc-koeln","borussia-dortmund","fc-schalke-04","borussia-moenchengladbach","fortuna-duesseldorf","sc-paderborn-07",
"tsg-1899-hoffenheim","1-fc-union-berlin","eintracht-frankfurt","1-fsv-mainz-05","fc-augsburg","hertha-bsc","sport-club-freiburg",
"vfl-wolfsburg","bayer-04-leverkusen","fc-bayern-muenchen","rb-leipzig","sv-werder-bremen"]

d_apr_team_averages = []
d_ir_team_averages = []
d_s_team_averages = []
N_ap_team_averages = []
for team_name in team_names:
	with open(team_name + ".csv") as csv_file:
    		csv_reader = csv.reader(csv_file, delimiter=',')
    		d_apr_team_average = 0
    		d_ir_team_average = 0
    		d_s_team_average = 0
    		N_ap_team_average = 0
    		row_count = 0
    		for row in csv_reader:
    			if row_count != 0:
    				d_apr_team_average += float(row[33]) - float(row[27])
    				d_ir_team_average += float(row[27])
    				d_s_team_average += float(row[28])
    				N_ap_team_average += float(row[18])/float(row[19])	
    			row_count += 1	
    	csv_file.close()
    	d_apr_team_averages.append(d_apr_team_average/float(row_count-1))
    	d_ir_team_averages.append(d_ir_team_average/float(row_count-1))
    	d_s_team_averages.append(d_s_team_average/float(row_count-1))
    	N_ap_team_averages.append(N_ap_team_average/float(row_count-1))

d_apr_normalization = get_average(d_apr_team_averages)
d_ir_normalization = get_average(d_ir_team_averages)
d_s_normalization = get_average(d_s_team_averages)
N_ap_normalization = get_average(N_ap_team_averages)



final_d_aprs = []
final_d_irs = []
final_d_ss = []
final_N_aps = []
final_f_dms = []
final_f_cds = []
all_teams_strategy_scores = []
for team_name in team_names:

	with open(team_name + ".csv") as csv_file:
    		csv_reader = csv.reader(csv_file, delimiter=',')
    		d_apr = []
    		d_ir = []
    		d_s = []
    		N_ap = []
    		#an indicator for N_dm containing 1 if the match was dominated and 0 otherwise
    		I_dm = []
    		#an indicator for N_cd containing 1 if the match as counter-dominated and 0 otherwise
    		I_cd = []
    		row_count = 0
    		for row in csv_reader:
    			if row_count != 0:
    				d_apr.append(inversion(normalization(float(row[33]) - float(row[27]),d_apr_normalization)))
    				d_ir.append(normalization(float(row[27]),d_ir_normalization))
    				d_s.append(normalization(float(row[28]),d_s_normalization))
    				N_ap.append(inversion(normalization(float(row[18])/float(row[19]),N_ap_normalization)))
    				f_pp = float(row[23])
    				if f_pp > 65.0:
    					I_dm.append(1.0)
    				else:
    					I_dm.append(0.0)
    				if f_pp < (100.0 - 65.0) and float(row[0]) > float(row[1]):
    					I_cd.append(1.0)
    				else:
    					I_cd.append(0.0)
    			row_count += 1
		csv_file.close()

	num_of_matches = row_count-1	
	d_apr_rob = []
	d_ir_rob = []
	d_s_rob = []
	N_ap_rob = []
	d_apr_averages = []
	d_ir_averages = []
	d_s_averages = []
	N_ap_averages = []
	f_dms = []
	f_cds = []
	strategy_scores = []
	for l in range(1, num_of_matches):
		d_apr_mean = l_average(d_apr,l)
		d_apr_averages.append(d_apr_mean)
		d_apr_std = l_std(d_apr,l,d_apr_mean)
		d_apr_index = d_apr_std/d_apr_mean
		d_apr_rob.append(np.exp(-d_apr_index))
		d_ir_mean = l_average(d_ir,l)
		d_ir_averages.append(d_ir_mean)
		d_ir_std = l_std(d_ir,l,d_ir_mean)
		d_ir_index = d_ir_std/d_ir_mean
		d_ir_rob.append(np.exp(-d_ir_index))
		d_s_mean = l_average(d_s,l)
		d_s_averages.append(d_s_mean)
		d_s_std = l_std(d_s,l,d_s_mean)
		d_s_index = d_s_std/d_s_mean
		d_s_rob.append(np.exp(-d_s_index))
		N_ap_mean = l_average(N_ap,l)
		N_ap_averages.append(N_ap_mean)
		N_ap_std = l_std(N_ap,l,N_ap_mean)
		N_ap_index = N_ap_std/N_ap_mean
		N_ap_rob.append(np.exp(-N_ap_index))
		f_dm = l_average(I_dm,l)
		f_dms.append(f_dm)
		f_cd = inversion(l_average(I_cd,l))
		f_cds.append(f_cd)
		strategy_scores.append(mu_ss(d_apr_mean,d_ir_mean,d_s_mean,N_ap_mean,f_dm,f_cd))
	final_d_aprs.append(d_apr_averages[0])
	final_d_irs.append(d_ir_averages[0])
	final_d_ss.append(d_s_averages[0])
	final_N_aps.append(N_ap_averages[0])
	final_f_dms.append(f_dms[0])
	final_f_cds.append(f_cds[0])	
	all_teams_strategy_scores.append(strategy_scores)
	f = plt.figure()
	plt.subplot(221)
	plt.title("Robustness of d_apr")
	plt.plot(range(1,len(d_apr_rob)+1),d_apr_rob)
	plt.subplot(222)
	plt.title("Robustness of d_ir")
	plt.plot(range(1,len(d_ir_rob)+1),d_ir_rob)
	plt.subplot(223)
	plt.title("Robustness of d_s")
	plt.plot(range(1,len(d_s_rob)+1),d_s_rob)
	plt.subplot(224)
	plt.title("Robustness of N_ap")
	plt.plot(range(1,len(N_ap_rob)+1),N_ap_rob)
	plt.subplots_adjust(hspace = 0.5)
	f.savefig(team_name + ".pdf")
	plt.close()
	fss = plt.figure()
	plt.title("mu_ss")
	plt.plot(range(1,len(d_ir_rob)+1),strategy_scores)
	plt.xlabel("l")
	plt.ylabel("mu_ss")
	fss.savefig(team_name + "_mu_ss.pdf")
	plt.close()


	file_name = team_name + "_vars_and_measures.csv"
	with open(file_name, mode="w") as team_file:
			writer = csv.writer(team_file, delimiter=",")
			writer.writerow(["d_apr","d_ir","d_s","N_ap","f_dm","f_cd","ss"])
			for i in range(num_of_matches-1):
				writer.writerow([d_apr_averages[i],d_ir_averages[i],d_s_averages[i],N_ap_averages[i],f_dms[i],f_cds[i],strategy_scores[i]])
			team_file.close()

final_fig = plt.figure()
for ss in all_teams_strategy_scores:
	plt.plot(range(1,len(ss)+1),ss)
final_fig.savefig("all.pdf")
plt.close()

#analyze differences in features by plotting them as functions of l
#give higher weight to those with distinguishing power 

d_apr_league_average = get_average(final_d_aprs)
d_ir_league_average = get_average(final_d_irs)
d_s_league_average = get_average(final_d_ss)
N_ap_league_average = get_average(final_N_aps)
f_dm_league_average = get_average(final_f_dms)
f_cd_league_average = get_average(final_f_cds)

d_apr_std = get_population_std(d_apr_league_average,final_d_aprs)
d_ir_std = get_population_std(d_ir_league_average,final_d_irs)
d_s_std = get_population_std(d_s_league_average,final_d_ss)
N_ap_std = get_population_std(N_ap_league_average,final_N_aps)
f_dm_std = get_population_std(f_dm_league_average,final_f_dms)
f_cd_std = get_population_std(f_cd_league_average,final_f_cds)

dist_power_d_apr = d_apr_std/d_apr_league_average
dist_power_d_ir = d_ir_std/d_ir_league_average
dist_power_d_s = d_s_std/d_s_league_average
dist_power_N_ap = N_ap_std/N_ap_league_average
dist_power_f_dm = f_dm_std/f_dm_league_average
dist_power_f_cd = f_cd_std/f_cd_league_average
dist_power_norm = dist_power_d_apr + dist_power_d_ir + dist_power_d_s + dist_power_N_ap + dist_power_f_dm + dist_power_f_cd

weight1 = dist_power_d_apr/dist_power_norm
weight2 = dist_power_d_ir/dist_power_norm
weight3 = dist_power_d_s/dist_power_norm
weight4 = dist_power_N_ap/dist_power_norm
weight5 = dist_power_f_dm/dist_power_norm
weight6 = dist_power_f_cd/dist_power_norm

new_final_sss = []
for i in range(len(final_d_aprs)):
	current_ss = weight1 * g(final_d_aprs[i]) + weight2 * g(final_d_irs[i]) + weight3 * g(final_d_ss[i]) + weight4 * g(final_N_aps[i]) + \
	 			 weight5 * g(final_f_dms[i]) + weight6 * g(final_f_cds[i])
	new_final_sss.append(current_ss)

print "final_d_aprs"
print final_d_aprs
print "final_d_irs"
print final_d_irs
print "final_d_ss"
print final_d_ss
print "final_N_aps"
print final_N_aps
print "final_f_dms"
print final_f_dms
print "final_f_cds"
print final_f_cds
print "final_sss"
print new_final_sss

last_scores = []
for score in all_teams_strategy_scores:
	last_scores.append(score[0])

print "other last scores"
print last_scores