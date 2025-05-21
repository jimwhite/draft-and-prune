from z3 import *

# Variables
season_of_cookbook = Array('season_of_cookbook', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 5), And(season_of_cookbook[i] >= 0, season_of_cookbook[i] <= 1))))
solver.add(season_of_cookbook[2] != season_of_cookbook[5])
solver.add(season_of_cookbook[0] == season_of_cookbook[3])
solver.add(Implies(season_of_cookbook[0] == 0, season_of_cookbook[4] == 0))
solver.add(Implies(season_of_cookbook[2] == 0, season_of_cookbook[3] == 1))

# Answer choices
answer_choices = [
    ([0, 0], [1, 1]),  # A: K fall, L spring
    ([4, 0], [5, 1]),  # B: O fall, P spring
    ([5, 0], [1, 1]),  # C: P fall, L spring
    ([0, 1], [1, 1]),  # D: K spring, L spring
    ([2, 0], [1, 0])   # E: M fall, L fall
]

for choice_index, (fall_books, spring_books) in enumerate(answer_choices):
    solver.push()
    for book in fall_books:
        solver.add(season_of_cookbook[book] == 0)
    for book in spring_books:
        solver.add(season_of_cookbook[book] == 1)

    if solver.check() == sat:
        model = solver.model()
        unique_solution = True
        for i in range(6):
            solver.push()
            # The error was here: model[season_of_cookbook[i]] returns a Z3 value, not an integer index.
            # We need to evaluate the array at index i within the model.
            solver.add(season_of_cookbook[i] != model.eval(season_of_cookbook[i]))
            if solver.check() == sat:
                unique_solution = False
                solver.pop()
                break
            solver.pop()

        if unique_solution:
            print(f"Option {chr(65 + choice_index)} is correct")
            exit()

    solver.pop()

