from z3 import *

# Lab assistant indices: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
assistant_indices = {name: i for i, name in enumerate(assistants)}

# Session positions 0-5: Wed AM=0, Wed PM=1, Thu AM=2, Thu PM=3, Fri AM=4, Fri PM=5
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each assistant assigned a unique session position 0-5
solver.add(Distinct(*pos))
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)

# Helper expressions for day and slot using Z3 division
day = [Int(f"day_{i}") for i in range(6)]
slot = [Int(f"slot_{i}") for i in range(6)]

# Relate pos, day, and slot
for i in range(6):
    solver.add(day[i] == pos[i] / 2)
    solver.add(slot[i] == pos[i] % 2)

# Constraints
## Kevin and Rebecca must lead sessions on the same day
solver.add(day[assistant_indices["Kevin"]] == day[assistant_indices["Rebecca"]])

## Lan and Olivia cannot lead sessions on the same day
solver.add(day[assistant_indices["Lan"]] != day[assistant_indices["Olivia"]])

## Nessa must lead an afternoon session (slot = 1)
solver.add(slot[assistant_indices["Nessa"]] == 1)

## Julio's session must be on an earlier day than Olivia's
solver.add(day[assistant_indices["Julio"]] < day[assistant_indices["Olivia"]])

## Premise: Lan does NOT lead a Wednesday session (day != 0)
solver.add(day[assistant_indices["Lan"]] != 0)

# Answer choices: Rebecca, Olivia, Nessa, Kevin, Julio
answer_choices = ["Rebecca", "Olivia", "Nessa", "Kevin", "Julio"]

# Check each answer choice
answer_index_list = []
for idx, name in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert this assistant is NOT on Thursday (day != 1)
    s_chk.add(day[assistant_indices[name]] != 1)
    
    # If UNSAT, then Thursday is forced for this assistant
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)