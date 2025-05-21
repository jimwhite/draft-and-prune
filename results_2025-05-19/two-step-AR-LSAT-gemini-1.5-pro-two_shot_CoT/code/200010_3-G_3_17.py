from z3 import *

# Variables
composition_at_slot = Array('composition_at_slot', IntSort(), IntSort())
F = 0
H = 1
L = 2
O = 3
P = 4
R = 5
S = 6
T = 7

# Solver
solver = Solver()

# Constraints
solver.add([And(composition_at_slot[i] >= 0, composition_at_slot[i] < 8) for i in range(8)])
solver.add(Distinct([composition_at_slot[i] for i in range(8)]))
# Use Store and Select to create a sequence for IndexOf
temp_seq = Select(composition_at_slot, IntVal(0))
for i in range(1,8):
    temp_seq = Store(temp_seq, IntVal(i), Select(composition_at_slot, IntVal(i)))

solver.add(Or(IndexOf(temp_seq, T) == IndexOf(temp_seq, F) - 1, IndexOf(temp_seq, T) == IndexOf(temp_seq, R) + 1))
solver.add(Or(IndexOf(temp_seq, R) - IndexOf(temp_seq, F) > 2, IndexOf(temp_seq, F) - IndexOf(temp_seq, R) > 2))
solver.add(Or(IndexOf(temp_seq, O) == 0, IndexOf(temp_seq, O) == 4))
solver.add(Or(composition_at_slot[7] == L, composition_at_slot[7] == H))
solver.add(IndexOf(temp_seq, P) < IndexOf(temp_seq, S))
solver.add(Or(IndexOf(temp_seq, S) - IndexOf(temp_seq, O) > 1, IndexOf(temp_seq, O) - IndexOf(temp_seq, S) > 1))
solver.add(composition_at_slot[2] == P)
solver.add(composition_at_slot[5] == S)

# Answer choices
options = [
    Or(composition_at_slot[4] == F, composition_at_slot[4] == H),
    Or(composition_at_slot[4] == F, composition_at_slot[4] == O),
    Or(composition_at_slot[4] == F, composition_at_slot[4] == T),
    Or(composition_at_slot[4] == H, composition_at_slot[4] == L),
    Or(composition_at_slot[4] == O, composition_at_slot[4] == R)
]

for i, option in enumerate(options):
    solver.push()
    solver.add(Not(option))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
