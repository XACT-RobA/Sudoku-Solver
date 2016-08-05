import math

DIM_X = 9
DIM_Y = 9

SUDOKU_GRID = ['0'] * (DIM_X * DIM_Y)

sample_grid_easy = [2,0,0,8,0,4,0,0,6,0,0,6,0,0,0,5,0,0,0,7,4,0,0,0,9,2,0,3,0,0,0,4,0,0,0,7,0,0,0,3,0,5,0,0,0,4,0,0,0,6,0,0,0,9,0,1,9,0,0,0,7,4,0,0,0,8,0,0,0,2,0,0,5,0,0,6,0,8,0,0,1]

sample_grid_medium = [0,0,0,3,0,4,0,0,0,0,1,2,0,0,0,8,9,0,0,6,0,0,0,0,0,2,0,6,0,0,0,5,0,0,0,4,0,0,0,1,0,7,0,0,0,3,0,0,0,6,0,0,0,1,0,9,0,0,0,0,0,5,0,0,7,8,0,0,0,6,4,0,0,0,0,9,0,8,0,0,0]

sample_grid_hard = [0,0,0,0,3,7,6,0,0,0,0,0,6,0,0,0,9,0,0,0,8,0,0,0,0,0,4,0,9,0,0,0,0,0,0,1,6,0,0,0,0,0,0,0,9,3,0,0,0,0,0,0,4,0,7,0,0,0,0,0,8,0,0,0,1,0,0,0,9,0,0,0,0,0,2,5,4,0,0,0,0]

for i in range(len(sample_grid_easy)):
    SUDOKU_GRID[i] = str(sample_grid_medium[i])

def disp_grid(grid):
    line_break = '-----------------------'
    print(line_break)
    for i in range(DIM_Y):
        this_line = '|'
        for j in range(DIM_X):
            index_position = (i * DIM_Y) + j
            char_to_display = grid[index_position]
            this_line += char_to_display
            if ((j % (DIM_X ** 0.5)) == 2):
                if  (j < DIM_X - 1):
                    this_line += '| |'
                else:
                    this_line += '|'
            else:
                this_line += '|'
        print(this_line)
        if (i % (DIM_Y ** 0.5)) == 2:
            print(line_break)
            
def get_ip(i, j):
    return (i * DIM_Y) + j

def get_coords(n):
    return [int(math.floor(n / DIM_Y)), n % DIM_X]

def get_sector(i, j):
    sector_i = math.floor(i / (DIM_Y**0.5))
    sector_j = math.floor(j / (DIM_X**0.5))
    return [sector_i, sector_j]

def get_possible_values(i, j, grid):
    all_valuess = '123456789'
    impossible_values = ''
    possible_values = ''
    # Get used values from row
    # Row is i
    for n in range(DIM_X):
        if n != j:
            this_row_val = grid[get_ip(i, n)]
            if this_row_val != '0':
                impossible_values += this_row_val
    
    # Get used values from column
    # Column is j
    for n in range(DIM_Y):
        if n != i:
            this_column_val = grid[get_ip(n, j)]
            if this_column_val != '0':
                if this_column_val not in impossible_values:
                    impossible_values += this_column_val
    
    # Get used values from sector
    this_sector = get_sector(i, j)
    for n in range(DIM_X * DIM_Y):
        iter_coord = get_coords(n)
        if n != get_ip(i, j):
            if get_sector(iter_coord[0], iter_coord[1]) == this_sector:
                this_sector_val = grid[n]
                if this_sector_val not in impossible_values:
                    impossible_values += this_sector_val

    for test_val in list(all_valuess):
        if test_val not in list(impossible_values):
            possible_values += test_val

    return possible_values

def get_all_possible_values(grid):
    possible_values = [''] * (DIM_X * DIM_Y)
    for i in range(DIM_Y):
        for j in range(DIM_X):
            index_position = get_ip(i, j)
            if grid[index_position] == '0':
                possible_values[index_position] = get_possible_values(i, j, grid)
    return possible_values

def update_element(input_grid):
    grid = []
    for value in input_grid:
        grid.append(value)
    # Get possible values for each element in the grid
    possible_values = get_all_possible_values(grid)
    # Set value if only one possible value
    for n in range(DIM_X * DIM_Y):
        if len(possible_values[n]) == 1:
            grid[n] = possible_values[n]
            return grid
            
    # Check possible values for each row
    for n in range(DIM_X * DIM_Y):
        if grid[n] == '0':
            this_coord = get_coords(n)
            remaining_possible_values = list(possible_values[n])
            for z in range(DIM_X):
                if z != this_coord[1]:
                    remaining_possible_values = list(set(remaining_possible_values) - set(list(possible_values[get_ip(this_coord[0], z)])))
            rem_poss_vals = ''.join(remaining_possible_values)
            if len(rem_poss_vals) == 1:
                grid[n] = rem_poss_vals
                return grid
    
    # Check possible values for each column
    for n in range(DIM_X * DIM_Y):
        if grid[n] == '0':
            this_coord = get_coords(n)
            remaining_possible_values = list(possible_values[n])
            for z in range(DIM_Y):
                if z != this_coord[0]:
                    remaining_possible_values = list(set(remaining_possible_values) - set(list(possible_values[get_ip(z, this_coord[1])])))
            rem_poss_vals = ''.join(remaining_possible_values)
            if len(rem_poss_vals) == 1:
                grid[n] = rem_poss_vals
                return grid
    
    # Check possible values for each sector
    for n in range(DIM_X * DIM_Y):
        if grid[0] == '0':
            this_sector = get_sector(get_coords(n)[0], get_coords(n)[1])
            remaining_possible_values = list(possible_values[n])
            for z in range(DIM_X * DIM_Y):
                if n != z:
                    if this_sector == get_sector(get_coords(z)[0], get_coords(z)[1]):
                        remaining_possible_values = list(set(remaining_possible_values) - set(list(possible_values[z])))
            rem_poss_vals = ''.join(remaining_possible_values)
            if len(rem_poss_vals) == 1:
                grid[n] = rem_poss_vals
                return grid
            
    return grid

if __name__ == '__main__':
    disp_grid(SUDOKU_GRID)
    print('')
    is_same = False
    old_grid = SUDOKU_GRID
    times_updated = 0
    while is_same == False:
        new_grid = update_element(old_grid)
        if old_grid == new_grid:
            is_same = True
            complete = True
            for n in range(DIM_X * DIM_Y):
                if new_grid[n] == '0':
                    complete = False
            if complete == True:
                print('Solved in ' + str(times_updated) + ' iterations')
            else:
                print('Failed to solve after ' + str(times_updated) + ' iterations')
                disp_grid(get_all_possible_values(new_grid))
        else:
            old_grid = new_grid
            times_updated += 1
    print('')
    disp_grid(new_grid)
