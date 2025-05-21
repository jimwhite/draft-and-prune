from z3 import *

# Define variables
season_of_cookbook = Array('season_of_cookbook', IntSort(), IntSort())

# Define constraints
def constraints(solver):
    i = Int('i')
    solver.add(ForAll([i], Implies(And(i >= 0, i < 6), And(season_of_cookbook[i] >= 0, season_of_cookbook[i] < 2)))) # Domain constraint
    solver.add(season_of_cookbook[2] != season_of_cookbook[5]) # M and P different seasons
    solver.add(season_of_cookbook[0] == season_of_cookbook[3]) # K and N same season
    solver.add(Implies(season_of_cookbook[0] == 0, season_of_cookbook[4] == 0)) # K in fall implies O in fall

# Get all solutions for the original problem
original_solver = Solver()
constraints(original_solver)
original_solver.add(Implies(season_of_cookbook[2] == 0, season_of_cookbook[3] == 1)) # Original condition

original_solutions = set()
while original_solver.check() == sat:
    model = original_solver.model()
    solution = tuple(model[season_of_cookbook[i]].as_long() for i in range(6))
    original_solutions.add(solution)
    original_solver.add(Or([season_of_cookbook[i] != model[season_of_cookbook[i]] for i in range(6)]))

# Check each answer choice
options = [
    Implies(season_of_cookbook[1] == 0, season_of_cookbook[2] == 1), # A
    Implies(season_of_cookbook[3] == 0, season_of_cookbook[5] == 0), # B
    Implies(season_of_cookbook[2] == 1, season_of_cookbook[5] == 0), # C
    Implies(season_of_cookbook[3] == 1, season_of_cookbook[2] == 1), # D
    Implies(season_of_cookbook[4] == 1, season_of_cookbook[3] == 1)  # E
]

for i, option in enumerate(options):
    option_solver = Solver()
    constraints(option_solver)
    option_solver.add(option)

    option_solutions = set()
    while option_solver.check() == sat:
        model = option_solver.model()
        solution = tuple(model[season_of_cookbook[j]].as_long() for j in range(6))
        option_solutions.add(solution)
        option_solver.add(Or([season_of_cookbook[j] != model[season_of_cookbook[j]] for j in range(6)]))
    
    if original_solutions == option_solutions:
        print(f"Option {chr(65 + i)} is correct")
        exit()
