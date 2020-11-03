import sys

# evaluate the simplest expression with only one level (no brackets)
def eval_simple_expression(simple_list):
    start_string = ''.join(simple_list)
    
    ## 1. negations first (~)    
    # check for errors like simple_list ending with ~
    if(simple_list[-1] == '~'):
        sys.exit('Error! A string {} has ended with ~'.format(start_string))
    
    i=0
    while(i < len(simple_list)):
        if(simple_list[i] == '~'):
            if(simple_list[i+1] == '0'):
                # evaluate to 1 and simplify
                simple_list[i+1] = '1'
                del simple_list[i]                                            
            elif(simple_list[i+1] == '1'):
                # evaluate to 0 and simplify
                simple_list[i+1] = '0'
                del simple_list[i]
            else:
                # some error
                sys.exit('Error in string with ~')
        i += 1
         
    ## 2. conjuntions second (&)
    # check for errors like simple_list starting or ending with &
    if(simple_list[0]=='&' or simple_list[-1]=='&'):
        sys.exit('Error! A string {} has ended or begun with &'.format(start_string))

    while(True):
        if('&' in simple_list):
            i = simple_list.index('&')
            # multiplication logic
            simple_list[i+1] = str(int(simple_list[i-1])*int(simple_list[i+1]))
            del simple_list[i-1:i+1]
        else:
            break
       
    # disjunctions last (|)
    # check for errors like simple_list starting or ending with |
    if(simple_list[0]=='|' or simple_list[-1]=='|'):
        sys.exit('Error! A string {} has ended or begun with |'.format(start_string))
        
    while(True):
        if('|' in simple_list):
            i = simple_list.index('|')
            # OR logic
            if(simple_list[i-1]=='1' or simple_list[i+1]=='1'):
                simple_list[i+1] = '1'                
            else:
                simple_list[i+1] = '0'
            
            # shorten the list in either case
            del simple_list[i-1:i+1]
        else:
            break
    
    # simple_list is simplified to the final answer
    return simple_list
    
# function to evaluate a boolean expression (may include parantheses) by breaking it into parts
def eval_bool_expression(bool_list):
    start_string = ''.join(bool_list)
    
    # error checking. if num of ('s doesn't match num of )'s
    if(bool_list.count('(') != bool_list.count(')')):
        sys.exit("Check parantheses in {}: # of ( and # of ) don't match".format(start_string))
        
    while(True):
        # exit when we've the final answer, i.e., len(bool_list)==1
        if(len(bool_list)==1):
            break
        
        left_ear = -1
        right_ear = -1        
        for i in range(len(bool_list)):
            if(bool_list[i] == '('):
                left_ear = i            
            elif(bool_list[i] == ')'):
                right_ear = i
                break

        # send entire bool_list if there are no parantheses
        if(left_ear==-1 and right_ear==-1):
            # the answer is a list of length 1. overwrite bool_list:
            bool_list = eval_simple_expression(bool_list)
        
        elif(left_ear==-1 or right_ear==-1):
            sys.exit('Error with parantheses in {}. Check carefully.'.format(start_string))        
        
        elif(left_ear < right_ear):
            bool_list[right_ear] = eval_simple_expression(bool_list[left_ear+1:right_ear])[0]            
            del bool_list[left_ear:right_ear]
        
        elif(left_ear > right_ear):
            sys.exit('Check parantheses order in {}. l = {}, r = {}'.format(''.join(bool_list), left_ear, right_ear))
        
        else:
            sys.exit('Error with parantheses in {}. Check carefully.'.format(start_string))

    # bool_list is now simplified to the final answer
    return bool_list

# read the var names file. store the names in a list
f_var_name = open('var_names.txt', 'r')
var_names = []
for line in f_var_name:
    s = line.strip()
    if(len(s)): #if > 0 
        var_names.append(s)

# read the equations
f_var_eqns = open('var_eqns.txt', 'r')
# there will be as many eqns as there are variables
var_eqns = ['' for x in range(len(var_names))]

for line in f_var_eqns:    
    # remove spaces from line. exclude empty lines
    line_without_spaces = line.strip() #remove space in end
    line_without_spaces = line_without_spaces.replace(' ', '') #remove space in middle
    if(len(line_without_spaces) == 0):
        continue
    
    # appending a newline character in the end, for parsing convenience
    line_without_spaces += '\n'
    
    # spot = sign in line_without_spaces
    for i in range(len(line_without_spaces)):
        if(line_without_spaces[i] == '='):
            break
    
    # define LHS and RHS
    eqn_lhs = line_without_spaces[0:i]
    eqn_rhs = line_without_spaces[i+1:]
    
    # parse the variable name on LHS. Raise error if name doesn't exist
    if(eqn_lhs not in var_names):
        sys.exit('Variable "{}" is undefined. Check var_names.txt\n'.format(eqn_lhs))
    
    # parse variable names on RHS. Raise error if any variable doesn't exist
    # eqn_rhs contains ~,&,|,(,) besides alphanumerics that make up var_names
    # there's a newline character at the end of line_without_spaces
    foo_var = ''    # empty string
    for ch in eqn_rhs:
        if(ch == '(' or ch == ')'):
            sys.exit('no "(" ")" allowed\n')
        if(ch in ['~', '&', '|', '(', ')','\n']):            
            # possibly end of one variable. check:
            if(len(foo_var)):
                # check if foo_var is in var_names. Raise error otherwise
                if(foo_var not in var_names):
                    sys.exit('Variable "{}" is undefined. Check var_eqns.txt'.format(foo_var))
                # reset foo_var                
                foo_var = ''
            # beginning of foo_var; go to the next character:
            else:                
                continue
            
        else:
            # add ch to foo_var
            foo_var += ch
                
    # passed the tests. match eqn_rhs (except the trailing newline) to its name
    var_eqns[var_names.index(eqn_lhs)] = eqn_rhs[:-1]

# print the result
for i in range(len(var_names)):    
    print('{} = {}'.format(var_names[i], var_eqns[i]))
#=====================================================================================================================
'''
# define the state of the variables (assume you already know num of variables)
state = [0,1,1,0,1]

## evaluating the equations!!


for each evaluation, define a new logical sentence replacing indices with boolean variables from state
recursively solve them starting from the innermost bracket. all this in a function, though.


# iterate through the equations
for i in range(len(var_eqns)):    
    expression_to_eval = var_eqns[i]
    for j in range(len(var_names)):
        expression_to_eval = expression_to_eval.replace(var_names[j], str(state[j]))
    
    res = eval_bool_expression(list(expression_to_eval))
    print('{} = {}'.format(res, expression_to_eval))
    # next step: state[i] = res    
'''