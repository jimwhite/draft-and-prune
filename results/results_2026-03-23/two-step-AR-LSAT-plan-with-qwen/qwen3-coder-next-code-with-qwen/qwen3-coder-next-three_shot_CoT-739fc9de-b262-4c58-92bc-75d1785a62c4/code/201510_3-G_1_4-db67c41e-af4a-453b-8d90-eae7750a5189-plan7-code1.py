from z3 import *

# Accomplice indices: 0=Peters, 1=Quinn, 2=Rovero, 3=Stanton, 4=Tao, 5=Villas, 6=White
pos = [Int(f"pos_{i}") for i in range(7)]

solver = Solver()

# Domain constraints: positions 1-7, all distinct
for i in range(7):
    solver.add(pos[i] >= 1, pos[i] <= 7)
solver.add(Distinct(*pos))

# Fixed constraint: Peters is recruited fourth
solver.add(pos[0] == 4)

# Villas immediately before White: pos[Villas] + 1 == pos[White]
solver.add(pos[5] + 1 == pos[6])

# Quinn immediately before Rovero (premise)
solver.add(pos[1] + 1 == pos[2])

# Stanton-Tao constraint: not adjacent
solver.add(Abs(pos[3] - pos[4]) != 1)

# Answer choices: ['first', 'second', 'third', 'fifth', 'seventh'] → positions 1,2,3,5,7
answer_positions = [1, 2, 3, 5, 7]
forbidden_indices = []

for idx, p in enumerate(answer_positions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    # Assert Stanton is in position p
    s_chk.add(pos[3] == p)
    
    if s_chk.check() == unsat:
        forbidden_indices.append(idx)

print(forbidden_indices)