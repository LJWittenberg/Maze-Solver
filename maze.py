from cell import Cell
import random
import time

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for i in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].Draw(x1,y1,x2,y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(len(self._cells) - 1, len(self._cells[0]) - 1)

    def _break_walls_r(self,i,j):
        self._cells[i][j].visited = True
        while True:
            directions = []

            #left
            if i > 0 and not self._cells[i-1][j].visited:
                directions.append((i-1,j))
            #right
            if i < self._num_cols-1 and not self._cells[i+1][j].visited:
                directions.append((i+1,j))
            #up
            if j > 0 and not self._cells[i][j-1].visited:
                directions.append((i,j-1))
            #down
            if j < self._num_rows-1 and not self._cells[i][j+1].visited:
                directions.append((i,j+1))
            # break condition
            if len(directions) == 0:
                self._draw_cell(i,j)
                return
            
            direction = random.randrange(len(directions))
            path = directions[direction]

            # right
            if path[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if path[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if path[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if path[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(path[0], path[1])

    def _reset(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        solved =  self._solve_r(0,0)
        if solved:
            return True
        return False

    def _solve_r(self,i,j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows -1:
            return True
        #left
        if i > 0 and not self._cells[i-1][j].visited and not self._cells[i-1][j].has_right_wall:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1,j):
                return True
            self._cells[i-1][j].draw_move(self._cells[i][j], True)
        #right
        if i < self._num_cols-1 and not self._cells[i+1][j].visited and not self._cells[i+1][j].has_left_wall:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1,j):
                return True
            self._cells[i+1][j].draw_move(self._cells[i][j], True)
        #up
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j-1].has_bottom_wall: 
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i,j-1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j-1], True)  
        #down
        if j < self._num_rows-1 and not self._cells[i][j+1].visited and not self._cells[i][j+1].has_top_wall:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i,j+1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j+1], True)

        return False