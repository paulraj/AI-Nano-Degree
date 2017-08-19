import collections

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """
    "Use naked twins propagation technique to reduce puzzle
    Input: The sudoku in dictionary form
    Output: Reduced sudoku puzzle in dictionary form
    """
    for units in unitlist:
        # Get values for each unit in list
        unit_values = [values[v] for v in units]
        # Find out all naked twin values
        naked_twins = [item for item, count in collections.Counter(unit_values).items() if count > 1 and len(item)==2]
        
        # If there is not any naked twins move to the next list of units
        if not naked_twins:
            continue
        
        #Loop through each unit in unitlist
        for unit in units:
            for twin in naked_twins:
                if values[unit] == twin:
                    continue
                #If the unit is not a naked twin, remove naked twin values
                for v in twin:
                    values[unit] = values[unit].replace(v,"")
    return values
    
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    digits = '123456789'
    for x in grid:
        if x == '.':    
            values.append(digits)
        elif x in digits:
            values.append(x)
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Use Elimination constraint propagation technique to eliminate values.
    Input: The sudoku in dictionary form
    Output: Reduced sudoku puzzle in dictionary form
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            #if len(values[peer]) > 1:  
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):    
    """
    Use Only Choice constraint propogation technique to reduce values.
    Input: The sudoku in dictionary form
    Output: Reduced sudoku puzzle in dictionary form
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iteratively use eliminate and only choice strategy.
    Input: The sudoku in dictionary form
    Output: Reduced sudoku puzzle in dictionary form
    """
    stalled = False
    while not stalled:
        number_of_valid_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        #print("number_of_valid_values_before: "+str(number_of_valid_values_before))
        #print("Before Eliminate Logic:")
        #display(values)
        values = eliminate(values)
        #print("\n\nPuzzle after Elimination logic:\n")
        #display(elim_grid_values) 
        #print("Before Only Choice Logic:")
        #display(values)
        values = only_choice(values)
        #print("\n\nPuzzle after Only-choice logic:\n")
        #display(only_choice_values)  
        #print("Before Twin peaks Logic:")
        #display(values)
        #values = naked_twins(values)
        #print("After Twin peaks Logic:")
        #display(values)
        number_of_valid_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        #print("number_of_valid_values_after: "+str(number_of_valid_values_after))
        stalled = number_of_valid_values_before == number_of_valid_values_after
		# Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
 
    return values

def search(values):
    """
    "Using depth-first search and propagation, try all possible values..
    Input: The sudoku in dictionary form
    Output: Reduced sudoku puzzle in dictionary form
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = search(grid_values(grid))
    #If puzzle is solved return the values in dictionary form, else return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    else:
        return False

def get_peers_for_diagonal():
    diagonals1 = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
    diagonals2 = ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']
    for d in diagonals1:
        others = [p for p in diagonals1 if p != d]
        peers[d] = peers[d].union(set(others))
        #print("peers for "+d+": "+str(peers[d]))
    for d in diagonals2:
        others = [p for p in diagonals2 if p != d]
        peers[d] = peers[d].union(set(others))
        #print("peers for "+d+": "+str(peers[d]))
    return peers


cols = '123456789'
rows = 'ABCDEFGHI'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# diag units for solving diagonal sudoku
diag_units = [[chr(64 + x) + str(x) for x in range(1,10)],[chr(74 - x) + str(x) for x in range(1,10)]]

square_units_dict = dict((s, [u for u in square_units if s in u]) for s in boxes)
square_units_peers = dict((s, set(sum(square_units_dict[s],[]))-set([s])) for s in boxes)
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    
    puzzle = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    naked_twin_puzzle = '84.632.....34798257..518.6...6.97..24.8256..12..84.6...8..65..3.54.2.7.8...784.96'
    naked_twin_puzzle2 = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    #display(solve(diag_sudoku_grid))
    display(solve(naked_twin_puzzle2))
    
    # g_values = grid_values(naked_twin_puzzle2)
    # display(g_values)
    # values = eliminate(g_values)
    # display(values)
    # values = eliminate(g_values)
    # display(values)
    # values = eliminate(g_values)
    # print("before naked Twin Results")
    # display(values)
    
    # values = naked_twins(values)
    # print("After naked Twin Results")
    # display(values)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
