import numpy as np

mrt = [4.0812, 4.0822 ,4.0680, 4.0492, 4.0508, 4.0356, 4.0309, 4.0221, 4.0190, 4.0017, 4.0007]
std = [0.0125, 0.0255 ,0.0328, 0.0173, 0.0139, 0.0261, 0.0229, 0.0141, 0.0104, 0.0213, 0.0266]

def compute(T, t, S, n):
	left = T - (t * S) / (n)**0.5
	right = T + (t * S) / (n)**0.5
	return left, right

#n = 10 # 10 replications
#t = 2.262 # according the t-distribution table
#
#for i in range(len(mrt)):
#	left, right = compute(mrt[i], t, std[i], n)
#	print("The 95% confident interval is [" + str(left) + ", " + str(right) + "].")

transient_end = 1000
number_of_jobs = 20000
baseline_system = []
improved_system = []
# read files
for i in range(1, 11):
	with open('tc0.1/trace' + str(i)) as f:
		response_time = [float(j) for j in f.read().splitlines()]
		mean_response_time = sum(response_time[transient_end:]) / (number_of_jobs - transient_end) - 2
		baseline_system.append(mean_response_time)
	with open('tc9.9/trace' + str(i)) as f:
		response_time = [float(j) for j in f.read().splitlines()]
		mean_response_time = sum(response_time[transient_end:]) / (number_of_jobs - transient_end)
		improved_system.append(mean_response_time)

print("    Index      	baseline_system-2	improved_system		improved_system-baseline_system")		
diff = []
for i in range(10):
	diff.append(improved_system[i] - baseline_system[i])
	print("replication" + str(i+1) + "	" + str(baseline_system[i]) + "	" + str(improved_system[i]) + "	" + str(improved_system[i] - baseline_system[i]))

mean = np.mean(diff)
std = np.std(diff)
n = 10 # 10 replications
t = 2.262 # according the t-distribution table
left,right = compute(mean, t, std, n)
print("The 95% confident interval is [" + str(left) + ", " + str(right) + "].")