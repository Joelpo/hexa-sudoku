import timeit
from HexaSudoku import sudoku
f = open("benchmark.txt")
read = str(f.read())
input_list = read.split()
test_list =[]
size = int(len(input_list)/256)
for i in xrange(1,size+1):
    test_list.append(input_list[256*(i-1):256+(256*(i-1))])
for i, test in enumerate(test_list):
    start = timeit.default_timer()
    sudoku(test)
    print "Test ",i," ran in ",timeit.default_timer()-start," s"
