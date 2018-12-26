import os
import random
import matplotlib.pyplot as plt
from simulation import RandomSimulation

# Random simulation for report
delayoff_time = 0.1  # fisrt step
#delayoff_times = [0.1, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0]  # second step
tc_list = []
mrt_list = []
while delayoff_time <= 15: # fisrt step
#for delayoff_time in delayoff_times: # second step
	tc_list.append(delayoff_time)
	sum_of_mrts = 0
	for i in range(1, 11): # 10 replications
		m = 5
		setup_time = 5.0
		time_end = 60000.0 # make it large enough to get about 20000 results
		
		arrival = 0.35
		service = 1.0
				
		master_clock = []
		dispatcher = [] # [arrival time, service time, marked or unmarked]
		server_state = [0] * m # 0:off, 1:set up, 2:busy, 3:delay off
		server_time = [-1] * m # intialize server times
		jobs = {} # [service time, depature time]
		
		random.seed(int(delayoff_time * i * 10))
		jobs = RandomSimulation(arrival, service, m, setup_time, delayoff_time, time_end, master_clock, dispatcher, server_state, server_time, jobs)
		response_times = []
		
		for job in jobs:
			if job < time_end and jobs[job][1] <= time_end and jobs[job][1] != -1:
				response_times.append(jobs[job][1] - job)
		
		mrt = sum(response_times) / len(response_times)
		sum_of_mrts += mrt
		
		# second step
		# current_dir = 'tc' + str(delayoff_time) # second step
		# if not os.path.exists(current_dir):
		# 	os.makedirs(current_dir)
		# with open(current_dir + '/trace' + str(i), 'w') as f:	
		# 	for i in range(20000):
		# 		f.write("%s\n" % response_times[i])
		
	mrt_of_10_replications = sum_of_mrts / 10
	mrt_list.append(mrt_of_10_replications)
	delayoff_time += 0.1

# first step
plt.plot(tc_list, mrt_list)
plt.axis([0, 16, 3.5, 6.5])
plt.grid(True)
plt.ylabel('Mean Response Time')
plt.xlabel('Delayoff Time')
plt.show()