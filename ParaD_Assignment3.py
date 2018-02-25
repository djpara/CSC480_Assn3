# David Para
# CSC 480
# Assignment 3

import re

def dp_run():
    first = ''.join(input(str("Please type first variable: ")).split(' '))
    if first.lower() == 'quit' or first.lower() == 'exit':
        raise SystemExit

    second = ''.join(input(str("Please type second variable: ")).split())
    if second.lower() == 'quit' or first.lower() == 'exit':
        raise SystemExit

    unification = dp_get_unification(first, second)

    print(unification)

def dp_get_unification(first, second):

    unification = dp_unify(first, second, [])

    if False in unification:
        return '\nFalse\n'

    unification = [item for item in unification if type(item) == str]
    unification = dp_format_unified_result(unification)

    return '\n%s\n' % ''.join(unification)

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
    elif dp_is_compound(x) or dp_is_compound(y):
        x_op = dp_get_op(x)
        x_args = dp_get_args(x)
        y_op = dp_get_op(y)
        y_args = dp_get_args(y)
        if x_op != y_op:
            if len(x_args) == 1:
                return dp_unify_var(x, y, s)
            if len(y_args) == 1:
                return dp_unify_var(y, x, s)
            # dp_unify(x_op, y_op, s)
        return dp_unify(x_args, y_args, s)
    elif type(x) == list and type(y) == list:
        if len(x) > 0 and len(y) > 0 and len(x) == len(y):
            dp_unify(x[0], y[0], s)
            return dp_unify(x[1:], y[1:], s)
        else:
            s.append(False)
            return s
    else:
        s.append(False)
        return s

def dp_unify_var(var, x, s):
    for n, item in enumerate(s):
        if item == None:
            s.remove(item)
            continue

        if var in item:
            val = item.split('/')[1]
            if val == x:
                continue
            if var == val:
                # If var already exists for value, replace current value so that we
                s[n] = item[:len(var)+1]+x
                continue
            return dp_unify(val, x, s)

        if x in item:
            val = item.split('/')[1]
            if x != val and x not in val:
                return dp_unify(var, val, s)

    if var == x:
        s.append(False)
        return s

    toAdd = "%s/%s" % (var, x)
    if toAdd not in s:
        s.append("%s/%s" % (var, x))
    return s

def dp_is_var(literal):
    return literal[0] == '?'

def dp_is_skolem(literal):
    return '?' in literal

def dp_is_compound(c):
    return '(' in c

def dp_is_var_val(literal):
    return '/' in literal

def dp_get_args(literal):
    return (''.join(re.split('(\()', literal)[1:])
                .replace(' ', '')[1:-1]).split(',')

def dp_get_op(literal):
    return re.split('[\(\/]', literal)[0]

def dp_format_unified_result(lst):
    e = len(lst)
    retval = ['{']
    for i, item in enumerate(lst):
        retval.append(item)
        if dp_is_var_val(item):
            if i < e - 1:
                retval.append(',')
            else:
                retval.append('}')
        i += 1
    return retval

print()

# RUNS THE PROGRAM
print('\nPlease type \'quit\' and press enter to exit at any time\n')
while (1):
    dp_run()

# TEST ALL
##def run_tests():
##
##    # Exception
##    first = "human(?x)"
##    second = "human(?y)"
##
##    print(dp_unify(first, second, None))
##    print()
##
##    # 1
##    first = "human(?x)"
##    second = "human(?y)"
##
##    print("#1: " + dp_get_unification(first, second))
##
##    # 2
##    first = "likes(?x,?y)"
##    second = "likes(pat0,chris2)"
##
##    print("#2: " + dp_get_unification(first, second))
##
##    # 3
##    first = "likes(?x,?x)"
##    second = "likes(pat0,chris2)"
##
##    print("#3: " + dp_get_unification(first, second))
##
##    # 4
##    first = "likes(?x,?x)"
##    second = "likes(?y,pat0)"
##
##    print("#4: " + dp_get_unification(first, second))
##
##    # 5
##    first = "likes(Pat0,Pat0)"
##    second = "likes(?x,?x)"
##
##    print("#5: " + dp_get_unification(first, second))
##
##    # 6
##    first = "likes(Pat0,?x)"
##    second = "likes(?y,Pat0)"
##
##    print("#6: " + dp_get_unification(first, second))
##
##    # 7
##    first = "likes(?x,?y,?y)"
##    second = "likes(pat0,chris)"
##
##    print("#7: " + dp_get_unification(first, second))
##
##    # 8
##    first = "likes(?x,?y)"
##    second = "likes(friend-of(Pat0),Pat0)"
##
##    print("#8: " + dp_get_unification(first, second))
##
##    # 9
##    first = "likes(friend-of(?y),?y)"
##    second = "likes(friend-of(?x),?x)"
##
##    print("#9: " + dp_get_unification(first, second))
##
##    # 10
##    first = "suburb(sk1(?c),?c)"
##    second = "suburb(?x,Naperville)"
##
##    print("#10: " + dp_get_unification(first, second))
##
##    # 11
##    first = "suburb(sk1(?c),?c)"
##    second = "suburb(skcity(?c),Naperville)"
##
##    # print("#11: " + dp_get_unification(first, second))
##
##    # 12
##    first = "suburb(sk1(?c),?c)"
##    second = "suburb(sk1(?c),Naperville)"
##
##    # print("#12: " + dp_get_unification(first, second))
##
##run_tests()

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
