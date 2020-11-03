import numpy as np
import sys

# function to update network_state
def parse_data(i_cond, tp):
    #node = 0    # index for nodes
    for node in range(NODE_NUM):
        curr_line = in_file.readline()
        
        # exit condition for the loop
        #if(node == NODE_NUM):
            #break
        
        node_state = (int)(curr_line.rstrip()[-1])
        if(node_state!=0 and node_state!=1):
            # error in parsing; exit the in_file            
            sys.exit("Error in parsing the file. Check data_parse.py")
        else:
            network_state[i_cond][tp][node] = node_state
            node += 1
                
    return


# NOTE: Add the parameters of the network, and the name of the file to parse, below:
INIT_COND = int(np.loadtxt('Initialization Setting.txt'))#500
TIME_STEP = int(np.loadtxt('Time Steps Setting.txt'))    #20+1   # {0,1,2...21}, for example. 0 = initial. 1,2,3.. = updates
TIME_STEP += 1

NODE_NUM = int(sum(1 for line in open('Node Name and their initial state.txt')) + 1) # 81

res_file_name = 'result.txt'
in_file = open(res_file_name, 'r')

output_file_name = 'net_after_parsing'

# start parsing!
network_state = np.zeros((INIT_COND, TIME_STEP, NODE_NUM), dtype='int8')

# indices (NOT the values in in_file) for initial condition, time
ic = 0
time = 0

ic_line = "initialization {}".format(ic+1)
update_line = "nodes' state after evaluating boolean equations in the above order:"

# read each line in in_file and add data to network_state
for line in in_file:
    # is line the beginning of a new ic?
    if(line.rstrip() == ic_line):
        
        # skip the next 2 lines
        # IMP: the top most line is popped each time in_file is iterated
        skip = 0
        for line_skip in in_file:
            # do nothing with line_skip
            skip += 1
            if(skip == 2):
                break
            
        # extract data from the next NODE_NUM lines. call the function        
        parse_data(ic, 0)    # time = 0 at this point        
        # update time
        time += 1
        
    # else: is the line the beginning of the results after one simulation time step?
    elif(line.rstrip() == update_line):
        # extract data from the next NODE_NUM lines. call the function
        parse_data(ic, time)
        
        # update time. if at the end of this initial condition, update ic too
        time += 1
        if(time == TIME_STEP):
            ic += 1
            ic_line = "initialization {}".format(ic+1)
            time = 0
    
in_file.close()  
np.save(output_file_name, network_state)
