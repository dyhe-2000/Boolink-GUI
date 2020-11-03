import numpy as np
import matplotlib.pyplot as plt
import sys

## LOADING STUFF
# file that contains all node names
f_all_node_name = open('Node Name and their initial state.txt', 'r')

# load the result array
bool_net = np.load('net_after_parsing.npy')

# file that has names of nodes to plot
f_plot_node_name = open('specific node.txt', 'r')


## PROCESSING DATA
# make a dictionary with node names
all_nodes = []
for line in f_all_node_name:
    for i in range(len(line)):
        if(line[i] in [' ', '\n']):
            s = line[0:i].strip()
            if(len(s)):
                all_nodes.append(s)
            break
    
num2name = dict([(i,all_nodes[i]) for i in range(len(all_nodes))])
name2num = dict([(all_nodes[i],i) for i in range(len(all_nodes))])

# read which nodes you want to plot
plot_nodes = []
for line in f_plot_node_name:
    s = line.strip()
    if(len(s)):
        plot_nodes.append(s)   
        
# some tests on all_nodes and plot_nodes
if(len(plot_nodes)==0):
    sys.exit('No node names to plot.')
    
for n in plot_nodes:
    if(n not in all_nodes):
        sys.exit('{} not found in the set of nodes. (Check spelling and formatting.)'.format(n))
        
# passed the tests!

# PLOT
t_list = range(bool_net.shape[1])   # points on time-axis
init_cond = bool_net.shape[0]       # number of initial conditions

plt.figure(1)
for n in plot_nodes:
    avg_act = 100*np.sum(bool_net[:,:,name2num[n]+1], axis=0)/init_cond
    plt.plot(t_list, avg_act)
    
plt.xlabel('Time')
plt.ylabel('Activity percentage')
plt.xticks(range(0,1+bool_net.shape[1],4))
plt.yticks(range(0,101,20))
plt.legend(plot_nodes)
plt.show()
