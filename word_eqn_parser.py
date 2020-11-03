import sys

node_name_file = 'Node Name and their initial state.txt'
word_eqn_file = 'Word Boolean Equations File.txt'
ind_eqn_file = 'Boolean Equations File.txt'

# read the var names file. store the names in a list
f_var_name = open(node_name_file, 'r')
var_names = []
for line in f_var_name:
    # remove any leading or trailing spaces
    s = line.strip()    
    if(len(s)):
        if(' ' in s):
            var_names.append(s[0:s.index(' ')])
        else:
            var_names.append(s)


# read the equations
f_var_eqns = open(word_eqn_file, 'r')
# there will be as many eqns as there are variables
var_eqns = ['' for x in range(len(var_names))]

for line in f_var_eqns:    
    # remove spaces from line. exclude empty lines
    line_without_spaces = line.strip()
    line_without_spaces = line_without_spaces.replace(' ', '')
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
    # eqn_rhs contains ~,&,| besides alphanumerics that make up var_names (and no parantheses!)
    # there's a newline character at the end of line_without_spaces
    eqn_with_indices = ''   # this will be the equation with names replaced with indices
    foo_var = ''            # empty string
    for ch in eqn_rhs:
        if(ch in ['~', '&', '|','\n']):            
            # possibly end of one variable. check:
            if(len(foo_var)):
                # check if foo_var is in var_names. Raise error otherwise
                if(foo_var in var_names):
                    eqn_with_indices += str(1 + var_names.index(foo_var))
                    eqn_with_indices += ch
                    # reset foo_var
                    foo_var = ''
                else:
                    sys.exit('Variable "{}" is undefined. Check var_eqns.txt'.format(foo_var))
                                
                                
            # beginning of foo_var; go to the next character:
            else:
                eqn_with_indices += ch
                continue
            
        else:
            # add ch to foo_var
            foo_var += ch
                
    # passed the tests. match eqn_rhs (except the trailing newline) to its name    
    var_eqns[var_names.index(eqn_lhs)] = eqn_with_indices[:-1]


# write the index-equations into a file
f_index_eqns = open(ind_eqn_file, 'w')
for expr in var_eqns:
    f_index_eqns.write(expr+'\n')
    
f_index_eqns.close()
f_var_eqns.close()
f_var_name.close()
