from z3 import *

# Variables
season_of_cookbook = Array('season_of_cookbook', IntSort(), IntSort())

# Solver
solver = Solver()

# Constraints
cookbooks = [0, 1, 2, 3, 4, 5]  # K, L, M, N, O, P
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i <= 5), And(season_of_cookbook[i] >= 0, season_of_cookbook[i] <= 1))))
solver.add(season_of_cookbook[2] != season_of_cookbook[5])  # M and P different seasons
solver.add(season_of_cookbook[0] == season_of_cookbook[3])  # K and N same season
solver.add(Implies(season_of_cookbook[0] == 0, season_of_cookbook[4] == 0))  # K in fall implies O in fall
solver.add(Implies(season_of_cookbook[2] == 0, season_of_cookbook[3] == 1))  # M in fall implies N in spring
solver.add(season_of_cookbook[2] == 0)  # M is published in the fall

# Answer choices
answer_choices = [
    ([0, 4], "A"),  # K and O
    ([1, 3], "B"),  # L and N
    ([1, 4], "C"),  # L and O
    ([3, 5], "D"),  # N and P
    ([4, 5], "E")   # O and P
]

for choice, option in answer_choices:
    solver.push()
    solver.add(season_of_cookbook[choice[0]] == 0)
    solver.add(season_of_cookbook[choice[1]] == 0)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()