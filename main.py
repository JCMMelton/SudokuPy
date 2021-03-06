
def not_zero(v):
    return v > 0


def no_zeros(value_list):
    return list(filter(not_zero, value_list))


def combine_sets(list_of_sets):
    c = set()
    for s in list_of_sets:
        c = c | s
    return c


puzzle_1 = [
    0, 7, 0,  0, 0, 0,  0, 2, 0,
    2, 0, 0,  5, 0, 1,  0, 0, 8,
    0, 0, 5,  0, 6, 0,  4, 0, 0,

    0, 6, 0,  9, 0, 7,  0, 5, 0,
    0, 0, 8,  0, 3, 0,  6, 0, 0,
    0, 4, 0,  2, 0, 6,  0, 8, 0,

    0, 0, 3,  0, 5, 0,  8, 0, 0,
    1, 0, 0,  3, 0, 8,  0, 0, 6,
    0, 9, 0,  0, 0, 0,  0, 3, 0
]

puzzle_2 = [
    0, 0, 3,  0, 9, 4,  0, 7, 8,
    2, 0, 7,  0, 0, 0,  1, 0, 0,
    0, 0, 1,  6, 0, 0,  0, 0, 3,

    0, 0, 5,  0, 0, 6,  0, 0, 1,
    7, 1, 0,  9, 0, 8,  0, 3, 2,
    9, 0, 0,  5, 0, 0,  6, 0, 0,

    1, 0, 0,  0, 0, 3,  9, 0, 0,
    0, 0, 9,  0, 0, 0,  7, 0, 6,
    6, 5, 0,  7, 8, 0,  3, 0, 0
]

puzzle_3 = [
    0, 2, 0,  0, 0, 0,  0, 4, 0,
    3, 0, 0,  8, 0, 0,  0, 0, 6,
    0, 0, 8,  6, 0, 3,  0, 0, 0,
                              
    0, 8, 9,  0, 0, 6,  3, 0, 0,
    0, 0, 0,  0, 7, 0,  0, 0, 0,
    0, 0, 7,  1, 0, 0,  2, 8, 0,

    0, 0, 0,  7, 0, 9,  1, 0, 0,
    8, 0, 0,  0, 0, 2,  0, 0, 5,
    0, 1, 0,  0, 0, 0,  0, 3, 0
]

puzzle_4 = [
    4, 0, 0,  6, 0, 3,  0, 0, 0,
    3, 0, 0,  0, 0, 0,  2, 0, 6,
    0, 1, 0,  8, 0, 0,  0, 4, 3,

    0, 0, 0,  0, 0, 8,  9, 0, 0,
    2, 0, 0,  0, 0, 0,  0, 0, 1,
    0, 0, 6,  3, 0, 0,  5, 0, 0,

    9, 4, 0,  0, 0, 2,  0, 1, 0,
    1, 0, 5,  0, 0, 0,  0, 0, 7,
    0, 0, 0,  1, 0, 4,  0, 0, 5
]

puzzle_5 = [
    0, 2, 8,  5, 6, 0,  0, 7, 9,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    7, 4, 5,  8, 0, 0,  0, 3, 0,

    0, 0, 0,  0, 8, 1,  0, 0, 0,
    3, 7, 0,  0, 0, 0,  0, 4, 2,
    0, 0, 0,  7, 3, 0,  0, 0, 0,

    0, 5, 0,  0, 0, 9,  6, 1, 7,
    0, 0, 0,  0, 0, 0,  0, 0, 0,
    4, 1, 0,  0, 7, 8,  3, 9, 0
]


class Cell:

    def __init__(self, index, value):
        self.value = value
        self.potential = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        if value != 0:
            self.potential = {value}
            self.potential.pop()
        self.index = index
        self.column = index % 9
        self.row = int(index/9)
        self.block = int(self.column/3)
        if int(self.row/3) == 1:
            self.block += 3
        elif int(self.row/3) == 2:
            self.block += 6

    def update_value(self):
        if self.value == 0 and len(self.potential) == 1:
            self.value = self.potential.pop()
            return True
        return False

    def print(self):
        spc = ' '
        if self.index < 10:
            spc += ' '
        print('index: '+str(self.index)+spc+' value: '+str(self.value)+' column: '+str(self.column)+'  row: '+
              str(self.row)+'  block: '+str(self.block))


class Board:

    def __init__(self, puz, fail_limit):
        self.failed = False
        self.solved = False
        self.fail = fail_limit
        self.runs = 0
        self.puzzle = puz
        self.cells = []
        for i in range(0, len(self.puzzle)):
            self.cells.append(Cell(i, self.puzzle[i]))
        self.percent = sum([1 for c in self.cells if not_zero(c.value)])

    def get_row(self, i):
        r = self.cells[i].row*9
        return [self.cells[x] for x in range(r, r+9)]

    def get_column(self, i):
        return [self.cells[x] for x in range(self.cells[i].column, 81, 9)]

    def get_block(self, i):
        block = self.cells[i].block
        return list(filter(lambda cell: block == cell.block, self.cells))

    def get_row_values(self, i):
        r = self.cells[i].row*9
        return no_zeros([self.cells[x].value for x in range(r, r+9)])

    def get_column_values(self, i):
        return no_zeros([self.cells[x].value for x in range(self.cells[i].column, 81, 9)])

    def get_block_values(self, i):
        block = self.cells[i].block
        return no_zeros([b.value for b in self.cells if b.block == block])

    def test_cell(self, i):
        self.gather_potentials(i)
        if self.cells[i].update_value():
            self.percent += 1

    def gather_potentials(self, i):
        rv = self.get_row_values(i)
        cv = self.get_column_values(i)
        bv = self.get_block_values(i)
        av = set(rv+cv+bv)
        self.cells[i].potential.difference_update(av)

    def pair_lock(self, i):
        locked = False
        if len(self.cells[i].potential) == 2:
            target = self.cells[i]
            for group in [set(self.get_row(i)), set(self.get_column(i)), set(self.get_block(i))]:
                group.difference_update({target})
                for cell in group:
                    if len(cell.potential) == 2:
                        if target.potential == cell.potential:
                            rd = group.difference({cell})
                            for _cell in rd:
                                _cell.potential.difference_update(cell.potential)
                            locked = True
        return locked

    def n_lock(self, i, n):
        locked = False
        for x in range(2, n + 1):
            if len(self.cells[i].potential) == x:
                target = self.cells[i]
                for group in [set(self.get_row(i)), set(self.get_column(i)), set(self.get_block(i))]:
                    group.difference_update({target})
                    locks = []
                    for cell in group:
                        if len(cell.potential) == x:
                            if target.potential == cell.potential:
                                locks.append(cell)
                            if len(locks) == x-1:
                                rd = group.difference(set(locks))
                                for _cell in rd:
                                    if _cell.value != 0:
                                        continue
                                    _cell.potential.difference_update(cell.potential)
                                locked = True
        return locked

    def single_eliminate(self, i):
        eliminated = False
        if self.cells[i].value == 0:
            potentials = [
                set(self.get_row(i)).difference({self.cells[i]}),
                set(self.get_column(i)).difference({self.cells[i]}),
                set(self.get_block(i)).difference({self.cells[i]})
            ]
            for potential_set in potentials:
                p = combine_sets([pot.potential for pot in potential_set])
                d = self.cells[i].potential.difference(p)
                if len(d) == 1:
                    self.cells[i].potential = d
                    self.cells[i].update_value()
                    eliminated = True
        return eliminated

    def test(self):
        self.solved = True
        for i in range(0, 81):
            if self.cells[i].value == 0:
                self.test_cell(i)
                if self.runs > 10:
                    if self.runs > 20:
                        self.n_lock(i, 4)
                    elif self.runs > 15:
                        self.n_lock(i, 3)
                    else:
                        self.n_lock(i, 2)
                    self.single_eliminate(i)
                self.solved = self.solved and not_zero(self.cells[i].value)
        self.runs += 1
        if self.runs >= self.fail:
            self.failed = True
        return self.solved

    def print(self):
        for cell in self.cells:
            cell.print()

    def show(self):
        bot_padding = '  ' if self.runs < 10 else ' ' if self.runs != 100 else ''
        top_padding = '  ' if self.percent < 10 else ' ' if self.percent != 81 else ''
        out = top_padding + str(int((self.percent/81)*100)) + '%  - - - - - - - - \n'
        for i in range(0, 81):
            cell = self.cells[i]
            out += str(cell.value)+' '
            if cell.column == 2 or cell.column == 5:
                out += '| '
            if (cell.row == 2 or cell.row == 5) and cell.column == 8:
                out += '\n- - - | - - - | - - -'
            if cell.column == 8:
                out += '\n'
        out += bot_padding + str(self.runs) + ' - - - - - - - - -\n'
        print(out)


b1 = Board(puzzle_3, 30)
# b2 = Board(puzzle_3, 20)
#
# for x in range(2):
#     b1.cells[x].potential = b2.cells[x].potential = {1, 2}
#
# b1.n_lock(0, 2)
# b2.pair_lock(0)
#
# for c in range(0, 9):
#     print([c, b1.cells[c].potential, b2.cells[c].potential])


b1.show()
while not b1.failed and not b1.solved:
    solved = b1.test()
    b1.show()

if b1.failed:
    print('Failed to solved in '+str(b1.runs)+' runs')
else:
    print('Solved in '+str(b1.runs)+' runs')
