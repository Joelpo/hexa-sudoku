from copy import deepcopy
import timeit

units = []
unitlist = []
squares = []
peers = {}
peers1 = peers.copy()
dict_domain = {}
backtrack_count = 0
prune_domain = {}
dict_domain1 = dict(dict_domain)
value = {}
state_space = 0
mRv_vars = []
input_list = []
grid_size = 16
default_value = "-1"
pruned_value = "-1"

'''To represent the two elements'''


def represent(A, B):
    return [a + b for a in A for b in B]


'''Initializes the sudoku function'''


def init_sudoku():
    cols = '0123456789ABCDEF'
    rows = 'ABCDEFGHIJKLMNOP'
    global squares
    squares = represent(rows, cols)
    global unitlist
    unitlist = ([represent(rows, c) for c in cols] + [represent(r, cols) for r in rows] + [represent(rs, cs) for rs in
                                                                                           ('ABCD', 'EFGH', 'IJKL',
                                                                                            'MNOP') for cs
                                                                                           in ('0123', '4567', '89AB',
                                                                                               'CDEF')])

    units = dict((s, [u for u in unitlist if s in u]) for s in squares)
    global peers
    peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)
    global dict_domain
    global value
    i = 0
    for s in squares:
        dict_domain[s] = ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
        value[s] = input_list[i]
        prune_domain[s] = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
        i = i + 1


'''Domain pruning for Backtrack'''


def domain_pruningBt(cellName, val):
    global dict_domain1
    global peers1
    peers1 = peers.copy()
    for elt in peers1[cellName]:
        if value[elt] == default_value:
            x = dict_domain[elt]
            if x[int(val) - 1] == "1":
                dict_domain[elt][int(val) - 1] = pruned_value
                prune_domain[elt][int(val) - 1] = cellName
    value[cellName] = str(hex(int(val)).split('x')[-1].upper())


'''Normal Domain Pruning'''


def domain_pruning(cellName, val):
    global peers1
    peers1 = peers.copy()
    for elt in peers1[cellName]:
        if dict_domain[elt][int(val, 16) - 1] == "1":
            dict_domain[elt][int(val, 16) - 1] = "0"


'''Assigns values initially from the given input'''


def assign_given_values():
    for i in xrange(len(input_list)):
        if input_list[i] != '-1':
            x = squares[i]
            if grid_size == 9:
                dict_domain[x] = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
            elif grid_size == 16:
                dict_domain[x] = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
            else:
                dict_domain[x] = ['0', '0', '0', '0']
            domain_pruning(x, input_list[i])
    return


'''Assigns values'''


def assign_values(pos, val):
    value[pos] = val
    domain_pruning(pos, val)


'''Assign values during Backtrack'''


def assign_valuesBt(pos, val):
    value[pos] = val
    domain_pruningBt(pos, val)


'''Unprunes for Backtrack'''


def unprune(cellName, val):
    global dict_domain1
    global peers1
    peers1 = peers.copy()
    for elt in peers1[cellName]:
        if dict_domain[elt][int(val) - 1] == "-1" and prune_domain[elt][int(val) - 1] == cellName:
            dict_domain[elt][int(val) - 1] = "1"
            prune_domain[elt][int(val) - 1] = ""


'''Funtion to provide MRV'''


def mRv(cell):
    global mRv_vars
    for elt in dict_domain[cell]:
        if elt == "1":
            assign_values(cell, str(hex(dict_domain[cell].index(elt) + 1).split('x')[-1].upper()))


'''Gets the element having minimum domain value'''


def get_minimum():
    count = 16
    for elt in dict_domain:
        if value[elt] == default_value:
            z = dict_domain[elt]
            a = z.count('1')
            if a < count:
                count = a
                key = elt
    if (count == 16):
        print ("min is 0")
    return key, count


'''Performs Arc Consistancy'''


def arcConsistent():
    while True:
        if solved() == True:
            return 0
        min_key, min_count = get_minimum()
        if min_count == 1:
            mRv(min_key)
            if solved() == True:
                return 0
        else:
            break
    return min_count


'''Performs Value lookup'''


def valToVar():
    rows = unitlist[16:32]
    cols = unitlist[0:16]
    boxes = unitlist[32:48]
    for r in rows:
        for i in xrange(1, grid_size + 1):
            count = 0
            pos = ""
            for cell in r:
                if cell in dict_domain.keys():
                    if value[cell] == default_value and dict_domain[cell][i - 1] == "1":
                        count += 1
                        if count == 1:
                            pos = cell
                if count > 1:
                    pos = ""
                    break
            if pos not in "":
                assign_values(pos, str(hex(i).split('x')[-1].upper()))
    for b in boxes:
        for i in xrange(1, grid_size + 1):
            count = 0
            pos = ""
            for cell in b:
                if cell in dict_domain.keys():
                    if value[cell] == default_value and dict_domain[cell][i - 1] == "1":
                        count += 1
                        if count == 1:
                            pos = cell
                if count > 1:
                    pos = ""
                    break
            if pos not in "":
                assign_values(pos, str(hex(i).split('x')[-1].upper()))
    for c in cols:
        for i in xrange(1, grid_size + 1):
            count = 0
            pos = ""
            for cell in c:
                if cell in dict_domain.keys():
                    if value[cell] == default_value and dict_domain[cell][i - 1] == "1":
                        count += 1
                        if count == 1:
                            pos = cell
                if count > 1:
                    pos = ""
                    break
            if pos not in "":
                assign_values(pos, str(hex(i).split('x')[-1].upper()))


'''Performs Value Lookup in Backtrack'''


def valToVarBT(minval):
    rows = unitlist[16:32]
    cols = unitlist[0:16]
    boxes = unitlist[32:48]
    for r in rows:
        for i in xrange(1, grid_size + 1):
            count = 0
            pos = ""
            for cell in r:
                if cell in dict_domain.keys():
                    if value[cell] == default_value and dict_domain[cell][i - 1] == "1":
                        count += 1
                        if count == 1:
                            pos = cell
                if count > 1:
                    pos = ""
                    break
            if pos not in "":
                prune_domain[pos][i - 1] = minval + 'VV'
                assign_valuesBt(pos, str(i))
                dict_domain[pos][i - 1] = "-1"

    for b in boxes:
        for i in xrange(1, grid_size + 1):
            count = 0
            pos = ""
            for cell in b:
                if cell in dict_domain.keys():
                    if value[cell] == default_value and dict_domain[cell][i - 1] == "1":
                        count += 1
                        if count == 1:
                            pos = cell
                if count > 1:
                    pos = ""
                    break
            if pos not in "":
                prune_domain[pos][i - 1] = minval + 'VV'
                assign_valuesBt(pos, str(i))
                dict_domain[pos][i - 1] = "-1"

    for c in cols:
        for i in xrange(1, grid_size + 1):
            count = 0
            pos = ""
            for cell in c:
                if cell in dict_domain.keys():
                    if value[cell] == default_value and dict_domain[cell][i - 1] == "1":
                        count += 1
                        if count == 1:
                            pos = cell
                if count > 1:
                    pos = ""
                    break
            if pos not in "":
                prune_domain[pos][i - 1] = minval + 'VV'
                assign_valuesBt(pos, str(i))
                dict_domain[pos][i - 1] = "-1"


'''Performs Unprune of Value Lookup in Backtrack'''


def valtovarunpruneBt(minval):
    for elt in squares:
        for i in xrange(0, 16):
            if prune_domain[elt][i] == minval + 'VV':
                unprune(elt, int(value[elt], 16))
                value[elt] = default_value
                dict_domain[elt][i] = "1"
                prune_domain[elt][i] = ""


'''Forward checking'''


def forwardcheck(element):
    for elt in peers[element]:
        z = dict_domain[elt]
        if (z.count('0') == grid_size):
            continue
        a = z.count('1')
        if a < 1 and value[elt] == default_value:
            return False
    return True


'''To check if the sudoku is solved'''


def solved():
    for elt in value:
        if value[elt] == default_value:
            return False
    return True


'''Provides the LCV count'''


def get_lcv_count(ind, peer_list):
    count = 0
    for elt in peer_list:
        if dict_domain[elt][ind] == '1':
            count = count + 1
    return count


'''Gets the LCV'''


def lcv(x, cell):
    count = 50
    rt_index = -1
    for index in xrange(len(x)):
        if x[index] == '1':
            c = get_lcv_count(index, peers[cell])
            if c < count:
                count = c
                rt_index = index
    x[rt_index] = "-4"
    return rt_index


btcount = 1

'''Performs Backtracking'''


def backtracking():
    global btcount
    global backtrack_count
    global state_space
    ret = 0
    if solved():
        return 0
    tee = "bt"
    if solved():
        print "solved"
        return 0
    minval, micount = get_minimum()
    dict_lcv = deepcopy(dict_domain[minval])
    for z in xrange(len(dict_domain[minval])):
        if dict_domain[minval][z] == "1":
            i = lcv(dict_lcv, minval)
            assign_valuesBt(minval, str(i + 1))
            retval = forwardcheck(minval)
            if retval == False:
                pass
            else:
                btcount = btcount + 1
                valToVarBT(str(btcount))
                state_space += 1
                ret = backtracking()
            if retval == False or ret == -1:
                if ret == -1:
                    valtovarunpruneBt(str(btcount))
                    btcount = btcount - 1
                backtrack_count += 1
                unprune(minval, int(value[minval], 16))
                value[minval] = default_value
            elif ret == 0:
                return 0
    return -1


'''Performs Naked Twins'''


def naked_twins():
    naked_twin_dict = {}
    for unit in unitlist:
        # Build a dictionary/hash map to identify a naked twin pair
        vdict = {}
        for box in unit:
            # Identify box containing only 2 possibilities as a candidate for a naked twin
            if dict_domain[box].count('1') == 2:
                val = "".join(str(hex(i).split('x')[-1].upper()) for i, j in enumerate(dict_domain[box]) if j == '1')
                if not val in vdict:
                    vdict[val] = [box]
                else:
                    vdict[val].append(box)

        for key in vdict:

            if len(vdict[key]) == 2:
                if not key in naked_twin_dict:
                    naked_twin_dict[key] = [unit]
                else:
                    naked_twin_dict[key].append(unit)
    for key in naked_twin_dict:
        for unit in naked_twin_dict[key]:
            for box in unit:
                if value[box] == default_value:
                    val1 = "".join(
                        str(hex(i).split('x')[-1].upper()) for i, j in enumerate(dict_domain[box]) if j == '1')
                    if val1 != key:
                        if key[0] in dict_domain[box]:
                            dict_domain[box][int(key[0])] = '0'
                        if key[1] in dict_domain[box]:
                            dict_domain[box][int(key[1])] = '0'
    return


''' Function to diaplay the Sudoku Grid'''


def display(vals):
    cols = '0123456789ABCDEF'
    rows = 'ABCDEFGHIJKLMNOP'
    counts = 0
    print_value = []
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            if value[r + c] == '-1':
                counts += 1
            if value[r + c] == '10':
                # print("0"),
                print_value.append("0")
            else:
                # print(value[r + c]),
                print_value.append(value[r + c])
    return print_value


''' 
    Main function Sudoku(input)
    Input is a list of 256 characters from '-1' to 'F'
'''


def sudoku(input):
    global input_list
    input_list = input
    start = timeit.default_timer()
    init_sudoku()
    rows = unitlist[4:8]
    cols = unitlist[0:4]
    boxes = unitlist[8:12]
    assign_given_values()
    x = 0
    y = -1
    vals = [[key, value[key]] for key in sorted(value)]
    while True:
        prev = deepcopy(dict_domain)
        x = arcConsistent()
        valToVar()
        naked_twins()
        if prev == dict_domain:
            break

    ans = 1
    if x == 0:
        bvbbb = 0 # hacky fix, we're good
    else:
        ans = backtracking()
    if ans == -1:
        print "No solution for sudoku"
    end = timeit.default_timer()
    return (display(value), end - start)
    # print "Time taken =", end - start
    # print "Backtrack Count = ", backtrack_count
    # print "State Space Generated = ", state_space
    # display(value)
