
import sys
import math
from HexaSudoku import sudoku

## FOR TESTING
# input = '0xxxxxBA3X68X5XXXXBX9XDXFX0X4XXXXXXXXXFXXXXADX13XX3X7XXXXXCXXXEXDXX3XF8XXCX2XEXXC21XXXXB8XD5XXXX9XX86XXCXXAFXX74X0XX1XAXX4XXXX8DXXX6XXXXXEXXX397FEXXXX97XXXC5X6AXX9AXXXXBXXX8XDC8XXXDXCXXAXXXXFBXXXXXX5XXXXXXXCXXXX7CAXDX6EXXX3X1CX0EXXXD7XXA9XFEX4XX7XFXX5XX0XX'
# input = 'xxxxxxbaxX68X5XXXXBX9XDXFX0X4XXXXXXXXXFXXXXADX13XX3X7XXXXXCXXXEXDXX3XF8XXCX2XEXXC21XXXXB8XD5XXXX9XX86XXCXXAFXX74X0XX1XAXX4XXXX8DXXX6XXXXXEXXX397FEXXXX97XXXC5X6AXX9AXXXXBXXX8XDC8XXXDXCXXAXXXXFBXXXXXX5XXXXXXXCXXXX7CAXDX6EXXX3X1CX0EXXXD7XXA9XFEX4XX7XxXX5XX0XXx'

input = sys.argv[1].upper()
N = int(math.floor(math.sqrt(len(input)))) # calculate N : the number of rows/columns in the sudoku
size = int(N ** 2)
blockSize = int(math.floor(math.sqrt(N)))
input = input[:size] # parse so that we have the correct sudoku length
NULL_CHARS = ['x', 'X', '.']

# def main():
puzzle = []

# format input
nEmpty = 0
for item in input:
    if NULL_CHARS.count(item):
        puzzle.append('-1')
        nEmpty+=1
    else:
        puzzle.append(item)

# check sudoku format N must be 16
# solve sudoku
if N != 16 or nEmpty >= N ** 2:
    print('Error : Format not supported. Matrix cannot be empty ')
    print("N of rows is " + str(N))
    print("size = " + str(size))
    print("N of rows should be 16 for hexa sudoku")
else: 
    solution, timeTaken = sudoku(puzzle)

    solutionStr =''
    for i in solution:
        solutionStr += i

    print(solutionStr)
    print(timeTaken)

sys.stdout.flush()


# if __name__ == "__main__":
#     main()