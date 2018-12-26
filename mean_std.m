% Week 7, Q1, Part (a): Transient removal   

% load the traces 
load trace1 
load trace2 
load trace3 
load trace4 
load trace5
load trace6
load trace7 
load trace8 
load trace9 
load trace10

% put the traces in an array
nsim = 10;     % number of simulation
ndp = 20000;  % number of data points in each simulation
response_time_traces = zeros(nsim,ndp);
for i = 1:10
    eval(['response_time_traces(i,:) = trace',num2str(i),';']);
end    

% Drop the first one thousand points as the transient
% Compute the mean from data points 1001 to 20,000
mt = mean(response_time_traces(:,1001:end)');

% Find the mean and standard deviation of mt
mean(mt)
std(mt)








