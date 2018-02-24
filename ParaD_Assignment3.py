# David Para
# CSC 480
# Assignment 3

import re

# function UNIFY(x,y,s) returns a substitution to make x and y identical
# inputs:
# x, a var, const, list, or compound expression
# y (same)
# s, a substitution built up so far (optional, default is empty)
# if s = failure then return failure
# else if x = y then return s
# else if var(x) the return unify-var(x,y,s)
# else if var(y) then return unify-var(y,x,s)
# else if LIST(x) and LIST(y) then
# return UNIFY(x.REST,y.REST,UNIFY(x.FIRST,y.FIRST,s))
# else return False

def dp_unify(x, y, s=[]):
    if type(s) != list:
        print('error')
        return Exception("Invalid parameter exception")
    elif x == y:
        s.append(x)
        return s
    elif dp_is_var(x):
        return dp_unify_var(x, y, s)
    elif dp_is_var(y):
        return dp_unify_var(y, x, s)
    elif dp_is_compound(x) and dp_is_compound(y):
        x_op = dp_get_op(x)
        x_args = dp_get_args(x)
        y_op = dp_get_op(y)
        y_args = dp_get_args(y)
        dp_unify(x_op, y_op, s)
        return dp_unify(x_args, y_args, s)
    elif type(x) == list and type(y) == list:
        s.append(dp_unify(x[0], y[0], s))
        return dp_unify(x[1:], y[1:], s)
    else:
        return False

# function UNIFY-VAR(var,x,s) returns a substitution
# if {var/val} is in s then return UNIFY(val,x,s)
# else if {x/val} is in s then return UNIFY(var,val,s)
# else if OCCUR-CHECK(var,x) then return failure
# else return add {var/x} to s

def dp_unify_var(var, x, s):
    for n, item in enumerate(s):
        if item == None:
            s.remove(item)
            continue

        if var in item:
            val = item[len(var)+1:]
            if val == x:
                continue
            if var == val:
                s[n] = item[:len(var)+1]+x
                continue
            return dp_unify(val, x, s)
        if x in item:
            val = item[len(x)+1:]
            if x == val:
                continue
            return dp_unify(var, val, s)

    if var == x:
        return False

    toAdd = "%s/%s" % (var, x)
    if toAdd not in s:
        s.append("%s/%s" % (var, x))
    return s

    # if "%s/%s" % (var, x) in s:
    #     return dp_unify(x, x, s)
    # elif "%s/%s" % (x, var) in s:
    #     return dp_unify(var, var, s)
    # elif var == x:
    #     print('Cannot be unified')
    #     return False
    # else:
    #     return s.append("%s/%s" % (var, x))

def dp_is_var(literal):
    return literal[0] == '?'

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
    retval = []
    for item in lst:
        retval.append(item)
        if dp_is_var_val(item):
            if i < e - 1:
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

def dp_get_unification(first, second):

    unification = dp_unify(first, second, [])

    if False in unification:
        return '\nFalse\n'

    unification = [item for item in unification if type(item) == str]
    unification = dp_format_unified_result(unification)

    return '\n%s\n' % ''.join(unification)

def dp_run():
    first = ''.join(input(str("Please type first variable: ")).split(' '))
    if first.lower() == 'quit' or first.lower() == 'exit':
        raise SystemExit

    second = ''.join(input(str("Please type second variable: ")).split())
    if second.lower() == 'quit' or first.lower() == 'exit':
        raise SystemExit

    unification = dp_get_unification(first, second)

    print(unification)

    # 1.
    # human(?x) U
    # human(?y) = > {?x /?y}
    # 2.
    # likes(?x,?y) U
    # likes(pat0, chris2) = > {?x / pat0,?y / chris2}
    # 3.
    # likes(?x,?x) U
    # likes(pat0, chris2) = > false
    # 4.
    # likes(?x,?x) U
    # likes(?y, pat0) = > {?x / pat0, ?y / pat0}
    # 5.
    # likes(Pat0, Pat0)
    # U
    # likes(?x,?x) = > {?x / Pat0)
    # 6.
    # likes(Pat0,?x) U
    # likes(?y, Pat0) = > {?y / Pat0, ?x / Pat0}
    # 7.
    # likes(?x,?y,?y) U
    # likes(Pat0, Chris0) = > false


print()

# RUNS THE PROGRAM
# print('\nPlease type \'quit\' and press enter to exit at any time\n')
# while (1):
#     dp_run()

# TEST FULL

# Exception
first = "human(?x)"
second = "human(?y)"

print(dp_unify(first, second, None))
print()

# 1
first = "human(?x)"
second = "human(?y)"

print("#1: "+dp_get_unification(first, second))

# 2
first = "likes(?x,?y)"
second = "likes(pat0,chris2)"

print("#2: "+dp_get_unification(first, second))

# 3 TODO
first = "likes(?x,?x)"
second = "likes(pat0,chris2)"

print("#3: "+dp_get_unification(first, second))

# 4 TODO
first = "likes(?x,?x)"
second = "likes(?y,pat0)"

print("#4: "+dp_get_unification(first, second))

# 5 TODO
first = "likes(Pat0,Pat0)"
second = "likes(?x,?x)"

print("#5: "+dp_get_unification(first, second))

# 6
first = "likes(Pat0,?x)"
second = "likes(?y,Pat0)"

print("#6: "+dp_get_unification(first, second))

# 7 TODO
# first = "likes(?x,?y,?y)"
# second = "likes(pat0,chris)"
#
# print("#7: "+dp_get_unification(first, second))

# TEST dp_is_compound FUNCTION
##compound = 'human(?x)'
##not_compound = 'human?x'
##
##print(dp_is_compound(compound))               # Should return True
##print(dp_is_compound(not_compound))       # Should return False

# TEST dp_get_args FUNCTION
# first = 'human(?x)'
# second = 'human(?x, ?y)'
# third = 'human(?x, ?x, ?y)'
# fourth = 'human(?x, sko1(?x), ?y)'
#
# print(dp_get_args(first) == ['?x'])
# print(dp_get_args(second) == ['?x', '?y'])
# print(dp_get_args(third) == ['?x', '?x', '?y'])
# print(dp_get_args(fourth) == ['?x', 'sko1(?x)', '?y'])
#
# first = 'human(?x)'
# second = 'human(?y)'
# # result = dp_unify(first, second)
# result = [item for item in dp_unify(first, second, []) if type(item) == str]
# result = dp_format_unified_result(result)
# result = '%s\n' % ''.join(result)

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