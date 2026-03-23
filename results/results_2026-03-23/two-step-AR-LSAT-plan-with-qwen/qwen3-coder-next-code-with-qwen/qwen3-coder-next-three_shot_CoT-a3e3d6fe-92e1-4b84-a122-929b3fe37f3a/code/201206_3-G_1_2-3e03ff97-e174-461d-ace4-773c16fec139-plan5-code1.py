from z3 import *

# Assistant indices: 0-Julio, 1-Kevin, 2-Lan, 3-Nessa, 4-Olivia, 5-Rebecca
(JULIO, KEVIN, LAN, NESSA, OLIVIA, REBECCA) = range(6)

# Session positions: 0-WM, 1-WA, 2-TM, 3-TA, 4-FM, 5-FA
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each position between 0 and 5, all distinct
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)
solver.add(Distinct(*pos))

# Helper function to get day index (0-Wed, 1-Thurs, 2-Fri)
def day_index(pos_var):
    return pos_var / 2

# Helper function to check if position is afternoon (odd positions: 1,3,5)
def is_afternoon(pos_var):
    return pos_var % 2 == 1

# Kevin and Rebecca same day constraint
solver.add(day_index(pos[KEVIN]) == day_index(pos[REBECCA]))

# Lan and Olivia different day constraint
solver.add(day_index(pos[LAN]) != day_index(pos[OLIVIA]))

# Nessa afternoon constraint
solver.add(is_afternoon(pos[NESSA]))

# Julio earlier day than Olivia constraint
solver.add(day_index(pos[JULIO]) < day_index(pos[OLIVIA]))

# Premise: Lan does not lead Wednesday session (positions 0,1)
solver.add(Or(pos[LAN] != 0, pos[LAN] != 1))

# Answer choices: ['Rebecca', 'Olivia', 'Nessa', 'Kevin', 'Julio']
answer_choices = [REBECCA, OLIVIA, NESSA, KEVIN, JULIO]

# Check each answer choice
answer_index_list = []
for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this assistant does NOT lead any Thursday session (positions 2,3)
    s_chk.add(And(pos[assistant] != 2, pos[assistant] != 3))
    
    # If UNSAT, this assistant must lead a Thursday session
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)