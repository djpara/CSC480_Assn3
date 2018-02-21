# David Para
# CSC 480
# Assignment 3

import re

def dp_unify(x, y, s = []):
    if type(s) == Exception:
        print('error')
        return Exception("The two literals provided cannot be unified.")
    elif x == y:
        s.append(x)
        return s
    elif x[0] == '?':
        return dp_unify_var(x, y, s)
    elif y[0] == '?':
        return dp_unify_var(y, x, s)
    elif dp_is_compound(x) and dp_is_compound(y):
        x_op = dp_get_op(x)
        x_args = dp_get_args(x)
        y_op = dp_get_op(y)
        y_args = dp_get_args(y)
        s.append(dp_unify(x_op, y_op, s))
        return dp_unify(x_args, y_args, s)
    elif type(x) == list and type(y) == list:
        s.append(dp_unify(x[0], y[0], s))
        return dp_unify(x[1:], y[1:],  s)
    else:
        print('error')
        return Exception("The two literals provided cannot be unified.")

def dp_unify_var(var, x, s):
    if  "%s/%s" % (var, x)  in s:
        return dp_unify(x, x, s)
    elif "%s/%s" % (x, var) in s:
        return dp_unify(var, var, s)
    elif var == x:
        print('error')
        return Exception("The two literals provided cannot be unified.")
    else:
        return s.append("%s/%s" % (var, x))
                     
def dp_is_compound(c):
    return '(' in c

def dp_is_var_val(literal):
    return '/' in literal

def dp_get_args(literal):
    return (''.join(re.split('(\()', literal)[1:])
            .replace(' ', '')[1:-1]).split(',')

def dp_get_op(literal):
    return re.split('\(', literal)[0]

def dp_format_unified_result(lst):
    i = 0
    e = len(lst)
    retval =[]   
    for item in lst:
        retval.append(item)
        if dp_is_var_val(item):
            if i < e-1:
                retval.append(',')
            else:
                retval.append(')')
        else:
            if i < e:
                retval.append('(')
            else:
                retval.append(')')
        i += 1
    return retval

def dp_run():
    first = ''.join(input(str("Please type first variable: ")).split(' '))
    if first.lower() == 'quit' or first.lower() == 'exit':
        raise SystemExit
    
    second = ''.join(input(str("Please type second variable: ")).split())
    if second.lower() == 'quit' or first.lower() == 'exit':
        raise SystemExit
    
    unification = [item for item in dp_unify(first, second, []) if type(item) == str]
    unification = dp_format_unified_result(unification)
    print('\n%s\n' % ''.join(unification))


# RUNS THE PROGRAM
print('\nPlease type \'quit\' and press enter to exit at any time\n')
while(1):
    dp_run()

# TEST dp_is_compound FUNCTION
##compound = 'human(?x)'
##not_compound = 'human?x'
##
##print(dp_is_compound(compound))               # Should return True
##print(dp_is_compound(not_compound))       # Should return False

# TEST dp_get_args FUNCTION
##first = 'human(?x)'
##second = 'human(?x, ?y)'
##third = 'human(?x, ?x, ?y)'
##fourth = 'human(?x, sko1(?x), ?y)'
##
##print(dp_get_args(first) == ['?x'])
##print(dp_get_args(second) == ['?x', '?y'])
##print(dp_get_args(third) == ['?x', '?x', '?y'])
##print(dp_get_args(fourth) == ['?x', 'sko1(?x)', '?y'])

# TEST dp_unify_var FUNCTION
##first = 'human(?x)'
##second = 'human(?x, ?y)'
##third = 'cat(?x, ?x, ?y)'
##fourth = 'dog(?x, sko1(?x), ?y)'
##
##print(dp_get_op(first) == 'human')
##print(dp_get_op(second) == 'human')
##print(dp_get_op(third) == 'cat')
##print(dp_get_op(fourth) == 'dog')

# TEST dp_unify FUNCTION
##first = 'human'
##second = 'human'
##third = 'cat'
##
##print(dp_unify(first, second) == ['human'])
##print(type(dp_unify(first, third)) == Exception)

# TEST dp_is_var_val FUNCTION
##var_val = '?x/?y'
##not_var_val = 'human'
##
##print(dp_is_var_val(var_val) == True)
##print(dp_is_var_val(not_var_val) == False)

# TEST dp_unify FUNCTION
##first = 'human(?x)'
##second = 'human(?y)'
