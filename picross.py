import itertools, math

# unordered sequence of all 2-len partitions of integer n
def bipartitions(n): 
    for x in xrange(1,n/2+1):
        yield [x, n-x]
        yield [n-x, x]
        
# credit: David Eppstein (author)
def partitions(n):
    # base case of recursion: zero is the sum of the empty list
    if n == 0:
        yield []
        return
        
    # modify partitions of n-1 to form partitions of n
    for p in partitions(n-1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]
            
# unordered sequence of all partitions of integer n of length at least 3
# fairly hackish; not mathematical
def square_partitions(n):
    for p in partitions(n):
        if len(p) > 2:
            for L in set(itertools.permutations(p)):
                yield L

"""
Sequence of binary numbers at most n-bit containing exactly one run 
of 1s of length s.
Example: n=4, s=2, list(output): [0b11, 0b110, 0b1100]
"""
def plain_space(n, s):
    pred = lambda x: int(math.log(x,2)+1) <= n
    count = itertools.count(0)
    seq = (2**s - 1 << shift for shift in count)
    return itertools.takewhile(pred, seq)

def circle_space(n, s):
    pred = lambda x: x > 0 and int(math.log(x,2)+1) <= n
    for p in bipartitions(s):
        num = lambda x: (2**p[1]-1)*(2**(x+p[0])) + (2**p[0] - 1)
        count = itertools.count(1)
        seq = (num(x) for x in count)
        for y in itertools.takewhile(pred, seq):
            count2 = itertools.count(0)
            seq2 = (y*2**p for p in count2)
            for z in itertools.takewhile(pred, seq2):
                yield z

def square_space(n, s):
    pred = lambda x: x > 0 and int(math.log(x,2)+1) <= n
    for p in square_partitions(s):
        def num(*args):
            s = 2**p[-1] - 1
            for i, nums in enumerate(reversed(zip(p, args))):
                s += (2**nums[0] - 1)*(2**nums[1])*(2**int(math.log(s,2)+1))
            return s
        zeroes = sorted(list(itertools.product(range(1, n-s), repeat=len(p)-1)), key=sum)
        seq = (num(*z) for z in zeroes)
        for y in itertools.takewhile(pred, seq):
            count2 = itertools.count(0)
            seq2 = (y*2**p for p in count2)
            for z in itertools.takewhile(pred, seq2):
                yield z

""" returns True if the nth digit of b1 matches the nth digit of b2"""
def binary_digit_comparison(n, b1, b2):
    return ((b1 >> n-1) ^ (b2 >> n-1)) % 2 == 0

"""
input: L, list containing 0s, 1s, and 2s; s, number of solid blocks in
row; t, either 0 (plain), 1 (circle), or 2 (square)
For L, 0 corresponds to a definitely empty cell, 1 to a definitely solid,
and 2 to unsure either way.
output: new L with updated values according to comparison to all possible
solutions to the row
"""
def refresh_row(L, s, t):
    L = list(L)
    space_func = [plain_space, circle_space, square_space][t]
    def space_gen(n, s):
        for S in space_func(n, s):
            do_yield = True
            for i, n in enumerate(L):
                #if L[i] != 2 and b_str(S,len(L))[i] != str(L[i]):
                if L[i] != 2 and not binary_digit_comparison(i+1,S,L[i]*(2**len(L)-1)):
                    do_yield = False
            if do_yield: yield S
    #print map(bin,space_gen(len(L), s))
    for c in range(len(L)):
        if all(binary_digit_comparison(c+1, S, 2**len(L)-1) for S in space_gen(len(L), s)):
            L[c] = 1
        elif all(binary_digit_comparison(c+1, S, 0) for S in space_gen(len(L), s)):
            L[c] = 0
    return tuple(L)

def transpose(grid):
    return map(list,zip(*grid))

def pretty_print(grid):
    for row in grid:
        for c in row:
            print c,
        print


# input row numbers
# input row properties
# input column numbers
# input column properties
rnums = [5,1,1,1,1,1,3]
rprops = [0]*7
cnums = [2,2,7,1,1]
cprops = [1,1,0,0,0]
rows = zip(rnums, rprops)
cols = zip(cnums, cprops)
grid = [(2,)*len(cols)]*len(rows)
pretty_print(grid)
while any(2 in r for r in grid):
    print "START PASS"
    for i, row in enumerate(grid):
        #print grid, rows[i][0], rows[i][1]
        grid[i] = refresh_row(row, rows[i][0], rows[i][1])
        #print grid
    grid = transpose(grid)
    for i, row in enumerate(grid):
        grid[i] = refresh_row(row, cols[i][0], cols[i][1])
    grid = transpose(grid)
pretty_print(grid)


# scrap code????

#L = refresh_row([2, 2, 2, 2, 2, 1, 2, 2], 4, 0)
#print L
#quit()



#print map(bin,square_space(6, 4))
#quit()


#def flatten(it); return list(itertools.chain.from_iterable(it))
#def interlace(L1, L2): return flatten(zip(L1, L2)) + [L1[-1]]

#def bin_num(ones, zeroes, right_pad=0):
#    return (2**ones - 1)*(2**zeroes)*(2**right_pad)
               #s += bin_num(*nums, right_pad=int(math.log(s,2)+1))

#L=[bin(n)[2:] for n in square_space(10, 5)]
#for i in itertools.product(range(1, 3), repeat=3):
    #print i
#print L



