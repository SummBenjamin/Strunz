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


with open('1-fc-koeln.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    num_of_matches = 0
    d_ap = []
    d_ir = []
    d_s = []
    N_ap = []
    row_count = 1
    for row in csv_reader:
    	if row_count !=1:
    		d_ap.append(inversion(np.exp(-float(row[33]) + float(row[27]))))
    		d_ir.append(np.exp(-float(row[27])))
    		d_s.append(np.exp(-float(row[28])))
    		N_ap.append(inversion(np.exp(-float(row[18])/float(row[19]))))
    	row_count += 1
csv_file.close()

d_ir_rob = []
d_s_rob = []
N_ap_rob = []
for l in range(1,len(d_ir)):
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
plt.subplot(221)
plt.title("Robsustness of d_ir")
plt.plot(range(1,len(d_ir_rob)+1),d_ir_rob)
plt.subplot(222)
plt.title("\nRobsustness of d_s")
plt.plot(range(1,len(d_s_rob)+1),d_s_rob)
plt.subplot(223)
plt.title("\nRobsustness of N_ap")
plt.plot(range(1,len(N_ap_rob)+1),N_ap_rob)
plt.show()

    
