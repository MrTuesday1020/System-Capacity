# COMP9334 Project

import random
import math
import matplotlib.pyplot as plt

def TraceSimulation(arrival, service, m, setup_time, delayoff_time, master_clock, dispatcher, server_state, server_time, jobs):
	for i in range(len(arrival)):
		jobs[arrival[i]] = [service[i], -1]
		master_clock.append(arrival[i])

	master_clock = sorted(master_clock)
	
	while len(master_clock) != 0:
		current_time = master_clock[0]
		
		# if current time is a new arrival
		if current_time in jobs:
			# first check dispatcher
			# if dispatcher is not empty
			if len(dispatcher) != 0:
				# check server states
				# if off server exists
				if 0 in server_state:
					# set up the server
					index = server_state.index(0)
					server_state[index] = 1
					server_time[index] = current_time + setup_time
					master_clock.append(current_time + setup_time)
					master_clock = sorted(master_clock)					
					# mark this job and put it into dispatcher
					dispatcher.append([current_time, jobs[current_time][0], 'MARKED'])
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
				# if no off server
				else:
					dispatcher.append([current_time, jobs[current_time][0], 'UNMARKED'])
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
			# if dispatcher is empty
			elif len(dispatcher) == 0:
				# check server states
				# if delay off server exists, put this job to this server
				if 3 in server_state:
					# update the server information
					index = server_state.index(3)
					server_state[index] = 2
					server_delayoff_time = server_time[index]
					server_time[index] = current_time + jobs[current_time][0]
					# change the delay off time in master clock to job depature time
					index = master_clock.index(server_delayoff_time)
					master_clock[index] = current_time + jobs[current_time][0]
					master_clock = sorted(master_clock)
					# record the depature time
					jobs[current_time][1] = current_time + jobs[current_time][0]
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
				# else if off server exits
				elif 0 in server_state:
					# set up the server
					index = server_state.index(0)
					server_state[index] = 1
					server_time[index] = current_time + setup_time
					master_clock.append(current_time + setup_time)
					master_clock = sorted(master_clock)					
					# mark this job and put it into dispatcher
					dispatcher.append([current_time, jobs[current_time][0], 'MARKED'])
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
				else:
					dispatcher.append([current_time, jobs[current_time][0], 'UNMARKED'])
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
		# if current time is not arrival time, then this time must in server_time list
		else:
			index = server_time.index(current_time)
			state = server_state[index]
			# if state is 2, the server has just finished a job
			if state == 2:
				# if dispatcher is empty
				if len(dispatcher) == 0:
					# delay off this server
					server_state[index] = 3
					server_time[index] = current_time + delayoff_time
					master_clock.append(current_time + delayoff_time)
					master_clock = sorted(master_clock)
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
				else:
					# take the first job in dispatcher and don't change the state of this serve, just change the server_time
					job = dispatcher.pop(0)
					server_time[index] = current_time + job[1]
					master_clock.append(current_time + job[1])
					master_clock = sorted(master_clock)
					# record the depature time
					jobs[job[0]][1] = current_time + job[1]
					# if this job is unmarked, then do nothing, else we should consider further actions
					if job[2] == 'MARKED':
						# find whether an unmarked job exists or not
						unmarked_index = -1
						for i in range(len(dispatcher)):
							if dispatcher[i][2] == 'UNMARKED':
								unmarked_index = i
								break
						# if there is a unmarked job, mark this job
						if unmarked_index != -1:
							dispatcher[unmarked_index][2] = 'MARKED'
						# turn off the server which has the longest setup time
						else:
							longest_setup_time = -1
							longest_setup_time_server = -1
							for i in range(m):
								if server_state[i] == 1 and server_time[i] > longest_setup_time:
									longest_setup_time = server_time[i]
									longest_setup_time_server = i
							server_state[longest_setup_time_server] = 0
							server_time[longest_setup_time_server] = -1
							master_clock.remove(longest_setup_time)
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
			# if state is 1, the server has just finished set up, take the first job from dispatcher
			elif state == 1:
				job = dispatcher.pop(0)
				server_state[index] = 2
				server_time[index] = current_time + job[1]
				master_clock.append(current_time + job[1])
				master_clock = sorted(master_clock)
				# record the depature time
				jobs[job[0]][1] = current_time + job[1]
				# #print information
				#print(current_time, dispatcher, server_state, server_time)
			# otherwise, expiry of the countdown timer of a server in DELAYEDOFF state.
			else:
				server_state[index] = 0
				server_time[index] = -1
				# #print information
				#print(current_time, dispatcher, server_state, server_time)

		# remove current time from master clock
		master_clock.pop(0)
		
	return jobs
	
def RandomSimulation(arrival, service, m, setup_time, delayoff_time, time_end, master_clock, dispatcher, server_state, server_time, jobs):
	first_arrival = random.expovariate(arrival)
	first_service = random.expovariate(service) + random.expovariate(service) + random.expovariate(service)
	
	jobs[first_arrival] = [first_service, -1]
	master_clock.append(first_arrival)
	master_clock = sorted(master_clock)
	
	arrivals = {}
	services = {}
	
	bin = 1
	while bin <= 30:
		arrivals[bin] = 0
		services[bin] = 0
		bin += 1
		
	
	while master_clock[0] < time_end:
		current_time = master_clock[0]
		
		# if current time is a new arrival
		if current_time in jobs:
			new_arrival = random.expovariate(arrival) + current_time
			new_service = random.expovariate(service) + random.expovariate(service) + random.expovariate(service)
			
			temp1 = math.ceil(new_arrival-current_time)
			temp2 = math.ceil(new_service)
			
			if temp1 in arrivals:
				arrivals[temp1] += 1
			if temp2 in services:
				services[temp2] += 1
			
			jobs[new_arrival] = [new_service, -1]
			master_clock.append(new_arrival)
			master_clock = sorted(master_clock)
			# first check dispatcher
			# if dispatcher is not empty
			if len(dispatcher) != 0:
				# check server states
				# if off server exists
				if 0 in server_state:
					# set up the server
					index = server_state.index(0)
					server_state[index] = 1
					server_time[index] = current_time + setup_time
					master_clock.append(current_time + setup_time)
					master_clock = sorted(master_clock)					
					# mark this job and put it into dispatcher
					dispatcher.append([current_time, jobs[current_time][0], 'MARKED'])
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
				# if no off server
				else:
					dispatcher.append([current_time, jobs[current_time][0], 'UNMARKED'])
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
			# if dispatcher is empty
			elif len(dispatcher) == 0:
				# check server states
				# if delay off server exists, put this job to this server
				if 3 in server_state:
					# update the server information
					index = server_state.index(3)
					server_state[index] = 2
					server_delayoff_time = server_time[index]
					server_time[index] = current_time + jobs[current_time][0]
					# change the delay off time in master clock to job depature time
					index = master_clock.index(server_delayoff_time)
					master_clock[index] = current_time + jobs[current_time][0]
					master_clock = sorted(master_clock)
					# record the depature time
					jobs[current_time][1] = current_time + jobs[current_time][0]
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
				# else if off server exits
				elif 0 in server_state:
					# set up the server
					index = server_state.index(0)
					server_state[index] = 1
					server_time[index] = current_time + setup_time
					master_clock.append(current_time + setup_time)
					master_clock = sorted(master_clock)					
					# mark this job and put it into dispatcher
					dispatcher.append([current_time, jobs[current_time][0], 'MARKED'])
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
				else:
					dispatcher.append([current_time, jobs[current_time][0], 'UNMARKED'])
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
		# if current time is not arrival time, then this time must in server_time list
		else:
			index = server_time.index(current_time)
			state = server_state[index]
			# if state is 2, the server has just finished a job
			if state == 2:
				# if dispatcher is empty
				if len(dispatcher) == 0:
					# delay off this server
					server_state[index] = 3
					server_time[index] = current_time + delayoff_time
					master_clock.append(current_time + delayoff_time)
					master_clock = sorted(master_clock)
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
				else:
					# take the first job in dispatcher and don't change the state of this serve, just change the server_time
					job = dispatcher.pop(0)
					server_time[index] = current_time + job[1]
					master_clock.append(current_time + job[1])
					master_clock = sorted(master_clock)
					# record the depature time
					jobs[job[0]][1] = current_time + job[1]
					# if this job is unmarked, then do nothing, else we should consider further actions
					if job[2] == 'MARKED':
						# find whether an unmarked job exists or not
						unmarked_index = -1
						for i in range(len(dispatcher)):
							if dispatcher[i][2] == 'UNMARKED':
								unmarked_index = i
								break
						# if there is a unmarked job, mark this job
						if unmarked_index != -1:
							dispatcher[unmarked_index][2] = 'MARKED'
						# turn off the server which has the longest setup time
						else:
							longest_setup_time = -1
							longest_setup_time_server = -1
							for i in range(m):
								if server_state[i] == 1 and server_time[i] > longest_setup_time:
									longest_setup_time = server_time[i]
									longest_setup_time_server = i
							server_state[longest_setup_time_server] = 0
							server_time[longest_setup_time_server] = -1
							master_clock.remove(longest_setup_time)
					# #print information
					#print(current_time, dispatcher, server_state, server_time)
			# if state is 1, the server has just finished set up, take the first job from dispatcher
			elif state == 1:
				job = dispatcher.pop(0)
				server_state[index] = 2
				server_time[index] = current_time + job[1]
				master_clock.append(current_time + job[1])
				master_clock = sorted(master_clock)
				# record the depature time
				jobs[job[0]][1] = current_time + job[1]
				# #print information
				#print(current_time, dispatcher, server_state, server_time)
			# otherwise, expiry of the countdown timer of a server in DELAYEDOFF state.
			else:
				server_state[index] = 0
				server_time[index] = -1
				# #print information
				#print(current_time, dispatcher, server_state, server_time)

		# remove current time from master clock
		master_clock.pop(0)
	
	# draw arrival and service exponential distribution figure
#	x_arrival = []
#	y_arrival = []	
#	for item in arrivals:
#		x_arrival.append(item)
#		y_arrival.append(arrivals[item])
#	x_service = []
#	y_service = []	
#	for item in services:
#		x_service.append(item)
#		y_service.append(services[item])
	# arrival
#	plt.bar(x_arrival, y_arrival)
#	plt.ylabel('Number of arrival')
#	plt.xlabel('Bin of arrival')
#	title = 'Exponential distribution with arrival rate = ' + str(arrival)
#	plt.title(title)
#	plt.show()
	# service
#	plt.bar(x_service, y_service)
#	plt.ylabel('Number of service')
#	plt.xlabel('Bin of service')
#	title = 'Exponential distribution with service rate = ' + str(service)
#	plt.title(title)
#	plt.show()
		
	return jobs