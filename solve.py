def sudoku(grid):
    s9 = { 1,2,3,4,5,6,7,8,9 }
    def possiblemoves(board,x,y,i,j):
        return s9 - ( set(board[x]) | {r[y] for r in board} | {c for r in board[i:i+3] for c in r[j:j+3]})

    def solve(board,unfilled):
        if sudoku.solution != None: return # cuts 20% off the runtime
        if unfilled:
            x,y = unfilled[0]
            for n in possiblemoves(board,x,y,x//3*3,y//3*3):
                board[x][y] = n
                solve(board,unfilled[1:])
            board[x][y] = 0
        else:
            sudoku.solution = [row[:] for row in board]

    sudoku.solution = None
    solve(grid,[(x,y) for x in range(9) for y in range(9) if grid[x][y] == 0])
    if sudoku.solution:
        return sudoku.solution
    #    print('solved')
    #    print('\n'.join(str(row) for row in sudoku.solution))