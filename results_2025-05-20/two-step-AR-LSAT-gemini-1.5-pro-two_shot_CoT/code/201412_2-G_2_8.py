from z3 import *

# Entities and Mappings
F = 0
G = 1
H = 2
J = 3
L = 0
O = 1
S = 2
W = 3

# Variables
lecture_time = Array('lecture_time', IntSort(), IntSort())
historian_topic = Array('historian_topic', IntSort(), IntSort())
historian_time = Array('historian_time', IntSort(), IntSort())

# Solver
solver = Solver()
i = Int('i')

# Constraints
solver.add(Distinct([lecture_time[i] for i in range(4)]))
solver.add(ForAll([i], Implies(And(i >= 0, i <= 3), And(lecture_time[i] >= 1, lecture_time[i] <= 4))))
solver.add(Distinct([historian_topic[i] for i in range(4)]))
solver.add(ForAll([i], Implies(And(i >= 0, i <= 3), And(historian_topic[i] >= 0, historian_topic[i] <= 3))))
solver.add(Distinct([historian_time[i] for i in range(4)]))
solver.add(ForAll([i], Implies(And(i >= 0, i <= 3), And(historian_time[i] >= 1, historian_time[i] <= 4))))
solver.add(ForAll([i], Implies(And(i >= 0, i <= 3), historian_time[i] == lecture_time[historian_topic[i]])))
solver.add(lecture_time[O] < lecture_time[L])
solver.add(lecture_time[W] < lecture_time[L])
solver.add(historian_time[F] < lecture_time[O])
solver.add(historian_time[H] < historian_time[G])
solver.add(historian_time[H] < historian_time[J])
solver.add(lecture_time[W] == 3)

# Answer Choices
answer_choices = [
    (historian_topic[F] == W, 'A'),
    (historian_topic[G] == O, 'B'),
    (historian_topic[G] == S, 'C'),
    (historian_topic[H] == S, 'D'),
    (historian_topic[J] == L, 'E')
]

for constraint, option in answer_choices:
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        print(f"Option {option} is correct")
        exit()
    solver.pop()