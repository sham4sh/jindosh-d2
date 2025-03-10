from copy import deepcopy


colors  = ['red',  'green',   'white', 'purple', 'blue']
nations = ['dunwall',  'karnaca',   'fraeport', 'dabkova', 'valeton'] 
drinks    = ['beer',  'whiskey',   'wine', 'absinthe', 'rum']
trinkets = ['bird', 'ring', 'medal','snuff tin','diamond']
names   = ['winslow',  'marcolla',   'natsiou', 'contee', 'finch']

# Populate domain
domain = [1,2,3,4,5]
var_domain = {c:domain.copy() for c in colors}
var_domain.update({n:domain.copy() for n in nations})
var_domain.update({p:domain.copy() for p in drinks})
var_domain.update({ca:domain.copy() for ca in trinkets})
var_domain.update({j:domain.copy() for j in names})
var_all = list(var_domain.keys())

constr_eq = [ # Put all known connections here; ie, Finch is wearing red.
    ('finch', 'red'),
    ('green', 'wine'),
    ('karnaca', 'blue'),
    ('natsiou', 'ring'),
    ('fraeport', 'diamond'),
    ('contee', 'absinthe'),
    ('dunwall', 'rum'),
    ('marcolla', 'baleton'),
    
]


# Return true if variables have the same assignment - do not change!
def check_neq(names, var_assigned):
    if names[0] in var_assigned and names[1] in var_assigned:
        if var_assigned[names[0]] != var_assigned[names[1]]:
            #print('\t', names[0], '!=', names[1])
            return True
    return False

# Helper to check if assignments are unique - do not change!
def check_unique(list_val):
    if len(set(list_val)) == len(list_val):
        return True
    return False

# Check through all variables for uniqueness - do not change!
def check_different_values(var_assigned):
    v_c = [var_assigned[v] for v in var_assigned.keys() if v in colors]
    if len(v_c) > 1 and not check_unique(v_c):
        #print('colors not unique')
        return False
    v_n = [var_assigned[v] for v in var_assigned.keys() if v in nations]
    if len(v_n) > 1 and not check_unique(v_n):
        #print('nations not unique')
        return False
    v_p = [var_assigned[v] for v in var_assigned.keys() if v in drinks]
    if len(v_p) > 1 and not check_unique(v_p):
        #print('drinks not unique')
        return False
    v_j = [var_assigned[v] for v in var_assigned.keys() if v in trinkets]
    if len(v_j) > 1 and not check_unique(v_j):
        #print('trinkets not unique')
        return False
    v_ca = [var_assigned[v] for v in var_assigned.keys() if v in names]
    if len(v_ca) > 1 and not check_unique(v_ca):
        #print('names not unique')
        return False
    
    return True

# Check all constraints for valid assignment
def check_constraints(var_assigned):

    # check constraints that no two variables of the same type have the same value
    if not check_different_values(var_assigned):
        #print('Not equal constraint invalid') 
        return False

    ## Begin constraints here. 
    # For direct assignment, ie Winslow on the far left, check for equality with the position index.
    # For 'next to' check that the differences in the two indices equals one. If direction matters, make sure to put the right one
    # (the greater index) before the left. If direction does not matter, use the absolute value.

            
    if 'winslow' in var_assigned:
        # Winslow in the first seat on the left.
        if var_assigned['winslow'] != 1:
            return False
        # Winslow is next to purple
        if 'purple' in var_assigned:
            if abs(var_assigned['winslow']- var_assigned['purple']) != 1:
                return False
            
    if 'green' in var_assigned:
        # Green is next to white
        if 'white' in var_assigned:
            if abs(var_assigned['green']- var_assigned['white']) != 1:
                return False

    if 'karnaca' in var_assigned:
        # Karnaca  is next to bird
        if 'bird' in var_assigned:
            if abs(var_assigned['karnaca']- var_assigned['bird']) != 1:
                return False
            
    if 'dabkova' in var_assigned:
        # dabkova  is next to snuff tin
        if 'snuff tin' in var_assigned:
            if abs(var_assigned['snuff tin']- var_assigned['dabkova']) != 1:
                return False
            #dabkova is next to beer
        if 'beer' in var_assigned:
            if abs(var_assigned['beer']- var_assigned['dabkova']) != 1:
                return False
            
    if 'whiskey' in var_assigned:
        # whiskey in the center.
        if var_assigned['whiskey'] != 3:
            return False
            
    

    for c in constr_eq:
        if check_neq(c, var_assigned):
            #print(c[0], '!=', c[1])
            return False



    return True

var_unassigned = var_all
var_assigned = {}


# Selected from unassigned list according to MRV heuristic
def select_unassigned(var_domain, var_unassigned): # 
    # Select the variable from unassigned with least remaining values
    size_domain = {var: len(valid_domain) for (var, valid_domain) in var_domain.items() if var in var_unassigned} 
    select_var = min(size_domain.items(), key=lambda x:x[1])
    if len(select_var) == 0:
        print('Error select unassigned', select_var)
    return select_var[0]
    
# Select value order - no heuristic assigned
def select_value_order(var_domain, var):
    return var_domain[var] 

# Update all domains after assignment
def update_domain(var, val, var_domain):
    if var in colors:
        for c in colors:
            if c != var:
                var_domain[c].remove(val)
    if var in nations:
        for n in nations:
            if n != var:
                var_domain[n].remove(val)
    if var in drinks:
        for p in drinks:
            if p != var:
                var_domain[p].remove(val)
    if var in trinkets:
        for c in trinkets:
            if c != var:
                var_domain[c].remove(val)
    if var in names:
        for j in names:
            if j != var:
                var_domain[j].remove(val)

# Return true if all variables have at least one valid value, for forward check
def check_domain(var_domain):
    min_domain = min(var_domain.values())
    if min_domain == 0:
        return False
    else:
        return True


def print_solution(var_assigned):
    print(var_assigned)

# Recursive forward check
def forward_checking():
    global var_domain
    if len(var_unassigned) == 0: # Solution Found
        print(var_assigned)
        return True
        
    new_var      = select_unassigned(var_domain, var_unassigned)
    order_values = select_value_order(var_domain, new_var)

    var_unassigned.remove(new_var)
    copy_domain  = deepcopy(var_domain)

    for new_val in order_values:
           
            var_assigned[new_var] = new_val
            if not check_constraints(var_assigned): # Check if assignment is invalid
                continue
        
            update_domain(var_domain, new_var, new_val)
            if check_domain(var_domain) == True:
                if forward_checking(): # Recursive call
                    return True
           
            var_domain = deepcopy(copy_domain)
            
    # Update assigned list
    var_assigned.pop(new_var)     
    var_unassigned.append(new_var)
    return False # Recurse to backtrack


forward_checking()
print(check_constraints(var_assigned))

