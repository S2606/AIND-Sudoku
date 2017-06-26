assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


boxes = cross(rows, cols)
# Define row units of a sudoku
row_units = [cross(r, cols) for r in rows]
# Define column units of a sudoku
column_units = [cross(rows, c) for c in cols]
# Define square units of a sudoku
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# Define diagonal units of a sudoku
diagonal_units = [[x + y for x, y in zip(rows, cols)], [x + y for x, y in zip(rows, cols[::-1])]]
# Create a list of all units of a sudoku
unitlist = row_units + column_units + square_units + diagonal_units
# Create a dictionary of peers of each box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)


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
    """Eliminate values using the naked twins strategy.
    Input:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Output:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    naked_twin_dic = {}
    for unit in unitlist:
        # Build a dictionary to identify a naked twin pair
        vdic = {}
        for box in unit:
            # Identify box containing only 2 possibilities as a candidate for a naked twin
            if len(values[box]) == 2:
                if not values[box] in vdic:
                    vdic[values[box]] = [box]
                else:
                    vdic[values[box]].append(box)
        # Examine the dictionary to validate the candidates present as
        # naked twin pairs
        for key in vdic:
            # Condition for the candidate to be a naked twin pair
            if len(vdic[key]) == 2:
                if not key in naked_twin_dic:
                    naked_twin_dic[key] = [unit]
                else:
                    naked_twin_dic[key].append(unit)

    # Eliminate the naked twins as possibilities for their peers
    for key in naked_twin_dic:
        for unit in naked_twin_dic[key]:
            for box in unit:
                if values[box] != key:
                    assign_value(values, box, values[box].replace(key[0], ''))
                    assign_value(values, box, values[box].replace(key[1], ''))

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input:
        grid(string) - A grid in string form.
    Output:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Input:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
        Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
        Input:
            values(dict): A sudoku in dictionary form.
        Output:
            evalues(dict): The resulting sudoku in dictionary form.
        """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values


def only_choice(values):
    """
        Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
        Input:
            values(dict): A sudoku in dictionary form.
        Output:
            values(dict): The resulting sudoku in dictionary form.
        """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    """ Iterate eliminate(), naked_twins() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Input:
            values(dict): A sudoku in dictionary form.
        Output:
            values(dict): The resulting sudoku in dictionary form.
        """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """ Using depth-first search and constraint propagation, try all possible values.
        Input:
            values(dict): A sudoku in dictionary form.
        Output:
            The values dictionary containing a solved sudoku or False if sudoku could not be solved
        """
    values = reduce_puzzle(values)
    if values is False:
        return False  ## Failed
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
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
    Input:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Output:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    if values:
        return values
    else:
        return False


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
