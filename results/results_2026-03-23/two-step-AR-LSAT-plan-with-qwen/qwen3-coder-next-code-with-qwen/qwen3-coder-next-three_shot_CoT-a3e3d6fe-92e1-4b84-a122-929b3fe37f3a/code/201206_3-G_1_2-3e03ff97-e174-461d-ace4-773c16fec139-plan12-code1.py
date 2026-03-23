from z3 import *

# Assistant indices: 0=Julio, 1=Kevin, 2=Lan, 3=Nessa, 4=Olivia, 5=Rebecca
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
assistant_indices = {name: idx for idx, name in enumerate(assistants)}

# Session indices: 0=Wam, 1=wap, 2=Tam, 3=Tap, 4=Fam, 5=Fap
# Day mapping: 0,1 -> Wednesday; 2,3 -> Thursday; 4,5 -> Friday
def day(session_idx):
    return If(session_idx < 2, 0, 
              If(session_idx < 4, 1, 2))

# Position variables for each assistant
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: all positions distinct and in [0,5]
solver.add(Distinct(pos))
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)

# Kevin and Rebecca same day
solver.add(day(pos[1]) == day(pos[5]))

# Lan and Olivia different days
solver.add(day(pos[2]) != day(pos[4]))

# Nessa afternoon session (positions 1,3,5)
solver.add(Or(pos[3] == 1, pos[3] == 3, pos[3] == 5))

# Julio earlier than Olivia
solver.add(pos[0] < pos[4])

# Premise: Lan does not lead a Wednesday session (not positions 0 or 1)
solver.add(pos[2] != 0, pos[2] != 1)

# Answer choices: ['Rebecca', 'Olivia', 'Nessa', 'Kevin', 'Julio']
answer_choices = [5, 4, 3, 1, 0]  # indices for Rebecca, Olivia, Nessa, Kevin, Julio

# Check each answer choice
answer_index_list = []
for idx, assistant_idx in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert assistant does NOT lead any Thursday session (positions 2 or 3)
    s_chk.add(pos[assistant_idx] != 2, pos[assistant_idx] != 3)
    
    # If UNSAT, this assistant must lead a Thursday session
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)