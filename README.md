# Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A:  1)First the units containing naked twins are identified.
    2)Then following the Naked twin pair constraint, values are to be eliminated from the peers of the naked twin pair in those units.
    3)This can have the effect that some boxes are left with only a single choice after such elimination and hence are solved or also other naked twin pairs are created.
    4)Iterating the eliminate(), naked_twins(), only_choice() strategies forms our constraint propagation part of sudoku solving algorithm.


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A:  1)First identify boxes belonging to the two diagonal units.
    2)Then in eliminate(), naked_twins() and only_choice() strategies we consider the two diagonal units along with row, column, square units as part of constraint propagation for solving the diagonal sudoku problem.
