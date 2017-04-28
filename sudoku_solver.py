import sys
import copy

class SudokuSolver:
    """
    Solve Sudoku puzzle. Puzzle should be in the format: 
    7,8,,,,1,,,
    ,3,,,6,,5,,
    5,,,8,,,4,,3
    ,,,,,4,,,9
    ,4,,,,,,5,
    1,,,6,,,,,
    6,,5,,,3,,,4
    ,,2,,9,,,8,
    ,,,7,,,,6,1
    """
    def __init__(self, path_to_puzzle_file):
        """
        Parse sudoku csv file. Solve and print out solved sudoku puzzle. 
        :param path_to_puzzle_file:     expects CSV. Each row separated by a newline
        """
        self.difficulty = 0
        self.sudoku_puzzle_file = open(path_to_puzzle_file, 'r')
        self.rows = self.parse_sudoku_puzzle_file()
        self.map_data_structures()
        self.assert_data_is_valid()
        self.print_puzzle_with_blank_for_unknowns()
        self.solve(5)

        if self.is_solved():
            print "### SOLVED ###"
        self.print_puzzle_showing_number_of_possible_values_where_unknown()

    def solve(self,depth):
        number_of_unknows = self.reduce_unknowns()
        while not self.is_solved() and number_of_unknows > self.reduce_unknowns():
            number_of_unknows = self.reduce_unknowns()
        if self.is_solved():
            self.print_puzzle_with_blank_for_unknowns()
            quit()
        count = 0
        while not self.is_solved() and depth > 0:
            count += 1
            current_state = copy.deepcopy(self.rows)
            try:
                self.make_a_guess(count)
                self.solve(depth-1)
            except Exception as ex:
                self.rows = current_state
                self.map_data_structures()


    def make_a_guess(self, count):
        for row_index, row in enumerate(self.rows):
            for column, value in enumerate(row):
                if len(value) > 1:
                    for item in value:
                        if count == 0:
                            row[row_index][column] = [item]
                        else:
                            count -= 1

    def assert_data_is_valid(self):
        """
        Check that puzzle data follows Sudoku rules. 
        """
        assert (len(self.list_of_all_values) == 81)
        assert(len(self.rows) == 9)
        assert (len(self.columns) == 9)
        assert (len(self.squares) == 9)
        assert (self.row_value_to_index(0,0) == 0)
        assert (self.row_value_to_index(8, 8) == 80)
        assert (self.overlap_lists([1,2,3,5],[6,2,7,8]) == [2])
        for item in self.list_of_all_values:
            assert(len(item) >= 1)
        for row in self.rows:
            self.assert_group_can_be_solved(row)
        for column in self.columns:
            self.assert_group_can_be_solved(row)
        for square in self.squares:
            self.assert_group_can_be_solved(square)

    def map_data_structures(self):
        """
        Map data structures for columns, squares (3x3), and a list if the entire puzzle.
        """
        self.map_columns()
        self.map_squares()
        self.map_list_of_all_values()

    def assert_group_can_be_solved(self, group_of_nine):
        """
        Check that a given gorup of 9 (column, row, or 3x3 square) 
        :param group_of_nine: 
        :return: 
        """
        bucket = range(1,10)
        for possible_values in group_of_nine:
            for value in possible_values:
                if value in bucket:
                    bucket.remove(value)
        assert(len(bucket) == 0)

    def is_solved(self):
        for item in self.list_of_all_values:
            if len(item) > 1:
                return False
        return True

    def deduct(self):
        self.difficulty += .001
        self.check_rows()
        self.check_columns()
        self.check_squares()
        return self.get_ambiguity_rating()


    def print_puzzle_showing_number_of_possible_values_where_unknown(self):
        print('')
        if self.is_solved():
            print '\t### SOLVED ###\n'
        for row in self.rows:
            for value in row:
                if len(value) > 1:
                    sys.stdout.write(' ')
                    sys.stdout.write('|' + str(len(value)) + '|')
                    continue
                assert(len(value) == 1)
                sys.stdout.write('  ')
                sys.stdout.write(str(value[0]))
                sys.stdout.write(' ')
            sys.stdout.write('\n')
        print 'Total solved value: ' + str(self.get_solved_values_count())
        print 'Ambiguity rating: ' + str(self.get_ambiguity_rating())
        print 'Nodes searched (in 1000s): ' + str(self.difficulty)

        sys.stdout.write('\n\n')

    def print_puzzle_with_blank_for_unknowns(self):
        print('')
        if self.is_solved():
            print '\t### SOLVED ###\n'
        for row in self.rows:
            for value in row:
                if len(value) > 1:
                    sys.stdout.write(' ')
                    sys.stdout.write('| |')
                    continue
                assert(len(value) == 1)
                sys.stdout.write('  ')
                sys.stdout.write(str(value[0]))
                sys.stdout.write(' ')
            sys.stdout.write('\n')
        print 'Total solved value: ' + str(self.get_solved_values_count())
        print 'Ambiguity rating: ' + str(self.get_ambiguity_rating())
        print 'Nodes searched (in 1000s): ' + str(self.difficulty)

        sys.stdout.write('\n\n')

    def get_solved_values_count(self):
        count = 0
        for row in self.rows:
            for value in row:
                if len(value) == 1:
                    count += 1
        return count

    def get_ambiguity_rating(self):
        ambiguity = 0
        for row in self.rows:
            for value in row:
                if len(value) > 1:
                    ambiguity += len(value)
        return ambiguity

    def parse_sudoku_puzzle_file(self):
        full_grid = []
        line = self.sudoku_puzzle_file.readline()
        for i in range(0,9):
            line_list = line.replace('\n','').rsplit(',')
            assert(len(line_list) == 9)
            self.make_each_value_list(line_list)
            full_grid.append(line_list)
            line = self.sudoku_puzzle_file.readline()
        assert(len(full_grid) == 9)
        return full_grid

    def map_columns(self):
        self.columns = [[],[],[],[],[],[],[],[],[]]
        for row in self.rows:
            for index, value in enumerate(row):
                self.columns[index].append(value)

    def map_squares(self):
        self.squares = [[], [], [], [], [], [], [], [], []]
        self.squares[0] = self.rows[0][0:3] + self.rows[1][0:3] + self.rows[2][0:3]
        self.squares[1] = self.rows[0][3:6] + self.rows[1][3:6] + self.rows[2][3:6]
        self.squares[2] = self.rows[0][6:9] + self.rows[1][6:9] + self.rows[2][6:9]
        self.squares[3] = self.rows[3][0:3] + self.rows[4][0:3] + self.rows[5][0:3]
        self.squares[4] = self.rows[3][3:6] + self.rows[4][3:6] + self.rows[5][3:6]
        self.squares[5] = self.rows[3][6:9] + self.rows[4][6:9] + self.rows[5][6:9]
        self.squares[6] = self.rows[6][0:3] + self.rows[7][0:3] + self.rows[8][0:3]
        self.squares[7] = self.rows[6][3:6] + self.rows[7][3:6] + self.rows[8][3:6]
        self.squares[8] = self.rows[6][6:9] + self.rows[7][6:9] + self.rows[8][6:9]

    def map_list_of_all_values(self):
        self.list_of_all_values = []
        for row in self.rows:
            self.list_of_all_values = self.list_of_all_values + row

    def make_each_value_list(self, list):
        for index, value in enumerate(list):
            list[index] = [value]
            if list[index] == ['']:
                list[index] = range(1,10)
            else:
                list[index] = [int(value)]

    def row_value_to_index(self, row, col):
        return row * 9 + col

    def check_rows(self):
        values_not_in_row = range(1,10)
        for row_index, row in enumerate(self.rows):
            for value in row:
                if len(value) == 1:
                    values_not_in_row.remove(value[0])
            for column_index, value in enumerate(row):
                index = self.row_value_to_index(row_index, column_index)
                if len(value) > 1:
                    self.overlap_lists(self.list_of_all_values[index], values_not_in_row)
            values_not_in_row = range(1,10)

    def check_columns(self):
        values_not_in_column = range(1, 10)
        for column_index, column in enumerate(self.columns):
            for value in column:
                if len(value) == 1:
                    values_not_in_column.remove(value[0])
            for row_index, value in enumerate(column):
                index = self.row_value_to_index(row_index, column_index)
                if len(value) > 1:
                    self.overlap_lists(self.list_of_all_values[index], values_not_in_column)
            values_not_in_column = range(1, 10)

    def check_squares(self):
        map = [0,0,0,1,1,1,2,2,2]
        row_map = [0,0,0,3,3,3,6,6,6]
        values_not_in_square = range(1, 10)
        for square_index, square in enumerate(self.squares):
            for value in square:
                if len(value) == 1:
                    values_not_in_square.remove(value[0])
            for value_index, value in enumerate(square):
                index = self.row_value_to_index(row_map[square_index] + map[value_index], (square_index % 3) * 3 + value_index % 3)
                if len(value) > 1:
                    self.overlap_lists(self.list_of_all_values[index], values_not_in_square)
            values_not_in_square = range(1, 10)

    def overlap_lists(self, l1, l2):
        non_overlapping_items = []
        for item in l1:
            if item not in l2:
                non_overlapping_items.append(item)
        for item in non_overlapping_items:
            l1.remove(item)
        return l1



    def reduce_unknowns(self):
        for row_index, row in enumerate(self.rows):
            for column, values in enumerate(row):
                if len(values) > 1:
                    for value in values:
                        original_value = self.try_value(row_index, column, value)
                        self.rows = original_value
                        self.map_data_structures()
        return self.get_ambiguity_rating()

    def try_value(self, row, column, value):
        hold_value = copy.deepcopy(self.rows)
        self.rows[row][column] = [value]
        self.map_data_structures()
        try:
            ambiguity_rating = self.deduct()
            while ambiguity_rating != self.deduct():
                ambiguity_rating = self.deduct()
            self.assert_data_is_valid()
        except Exception as ex:
            hold_value[row][column].remove(value)
        return hold_value

def main():
    for arg in sys.argv[1:]:
        SudokuSolver(arg)

if __name__ == '__main__':
    main()