# COMP9334 Project

import random
import matplotlib.pyplot as plt
from simulation import RandomSimulation, TraceSimulation

######################  Simulation by reading files ######################
with open("num_tests.txt") as f:
	num_tests = int(f.readline())

for i in range(1, num_tests+1):
	mode_file = "mode_" + str(i) + ".txt"
	para_file = "para_" + str(i) + ".txt"
	arrival_file = "arrival_" + str(i) + ".txt"
	service_file = "service_" + str(i) + ".txt"
	with open(mode_file) as f:
		mode = f.readline()
	
	with open(para_file) as f:
		para = f.read().splitlines()
		m = int(para[0])
		setup_time = float(para[1])
		delayoff_time = float(para[2])
		if mode == "random":
			time_end = float(para[3])			
			
	master_clock = []
	dispatcher = [] # [arrival time, service time, marked or unmarked]
	server_state = [0] * m # 0:off, 1:set up, 2:busy, 3:delay off
	server_time = [-1] * m # intialize server times
	jobs = {} # [service time, depature time]
	
	if mode == "trace":
		with open(arrival_file) as f:
			arrival = [float(i) for i in f.read().splitlines()]
				
		with open(service_file) as f:
			service = [float(i) for i in f.read().splitlines()]
	
		jobs = TraceSimulation(arrival, service, m, setup_time, delayoff_time, master_clock, dispatcher, server_state, server_time, jobs)
		seq = []
		sum_response_time = 0
		joblist = []
		for job in jobs:
			joblist.append([jobs[job][1], job])
		joblist = sorted(joblist)
		for job in joblist:
			temp = '{0:.3f}'.format(job[1]) + '\t' + '{0:.3f}'.format(job[0]) + '\n'
			seq.append(temp)
			sum_response_time += job[0] - job[1]
		mrt = sum_response_time / len(jobs)
		
		with open('departure_' + str(i) + '.txt', 'w') as f:
			f.writelines(seq)
			
		with open('mrt_' + str(i) + '.txt', 'w') as f:
			f.write('{0:.3f}'.format(mrt))
		
	else:
		with open(arrival_file) as f:
			arrival = float(f.readline())
					
		with open(service_file) as f:
			service = float(f.readline())
			
		random.seed(int(delayoff_time * i * 10))
		jobs = RandomSimulation(arrival, service, m, setup_time, delayoff_time, time_end, master_clock, dispatcher, server_state, server_time, jobs)
		seq = []
		sum_response_time = 0
		count = 0
		joblist = []
		for job in jobs:
			joblist.append([jobs[job][1], job])
		joblist = sorted(joblist)
		for job in joblist:
			if job[0] < time_end and job[1] <= time_end and job[0] != -1:
				temp = '{0:.3f}'.format(job[1]) + '\t' + '{0:.3f}'.format(job[0]) + '\n'
				seq.append(temp)
				sum_response_time += job[0] - job[1]
				count += 1
		mrt = sum_response_time / count
		
		with open('departure_' + str(i) + '.txt', 'w') as f:
			f.writelines(seq)
			
		with open('mrt_' + str(i) + '.txt', 'w') as f:
			f.write('{0:.3f}'.format(mrt))


###################### Random simulation for report ######################
#delayoff_time = 0.1
#mrt_list = []
#tc_list = []
#while delayoff_time <= 15:
#	tc_list.append(delayoff_time)
#	sum_of_mrts = 0
#	for i in range(1, 11): # 10 replications
#		m = 5
#		setup_time = 5.0
#		time_end = 60000.0 # make it large enough to get about 20000 results
#		
#		arrival = 0.35
#		service = 1.0
#				
#		master_clock = []
#		dispatcher = [] # [arrival time, service time, marked or unmarked]
#		server_state = [0] * m # 0:off, 1:set up, 2:busy, 3:delay off
#		server_time = [-1] * m # intialize server times
#		jobs = {} # [service time, depature time]
#		
#		random.seed(int(delayoff_time * i * 10))
#		jobs = RandomSimulation(arrival, service, m, setup_time, delayoff_time, time_end, master_clock, dispatcher, server_state, server_time, jobs)
#		response_times = []
#		
#		for job in jobs:
#			if job < time_end and jobs[job][1] <= time_end and jobs[job][1] != -1:
#				response_times.append(jobs[job][1] - job)
#		
#		mrt = sum(response_times) / len(response_times)
#		sum_of_mrts += mrt
#		
#		current_dir = 'tc' + str(delayoff_time)
#		with open(current_dir + '/trace' + str(i), 'w') as f:	
#			for i in range(20000):
#				f.write("%s\n" % response_times[i])
#		
#	mrt_of_10_replications = sum_of_mrts / 10
#	mrt_list.append(mrt_of_10_replications)
#	delayoff_time += 0.1
#
#plt.plot(tc_list, mrt_list)
#plt.axis([0, 16, 3.5, 6.5])
#plt.grid(True)
#plt.ylabel('Mean Response Time')
#plt.xlabel('Delayoff Time')
#plt.show()
	