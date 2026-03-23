from z3 import *

# Bird types: 0-oystercatchers, 1-petrels, 2-rails, 3-sandpipers, 4-terns
# Time slots: 0-indexed (0=1st, 1=2nd, ..., 4=5th)

# Variables for lecture type at each slot
slot = [Int(f"slot_{i}") for i in range(5)]

# Variables for hall at each slot: True=Gladwyn, False=Howard
hall = [Bool(f"hall_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Domain constraints: each slot has a distinct bird type (permutation)
solver.add(Distinct(*slot))

# Each slot must be assigned one of the 5 bird types
for i in range(5):
    solver.add(Or(slot[i] == 0, slot[i] == 1, slot[i] == 2, slot[i] == 3, slot[i] == 4))

# Fixed hall constraints
solver.add(hall[0] == True)      # First lecture in Gladwyn Hall
solver.add(hall[3] == False)     # Fourth lecture in Howard Auditorium

# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[i], 1, 0) for i in range(5)]) == 3)

# Sandpiper constraints
# Find position of sandpipers (value 3)
sand_pos = [Int(f"sand_pos_{i}") for i in range(5)]
for i in range(5):
    solver.add(sand_pos[i] == If(slot[i] == 3, i + 1, 0))
solver.add(Sum(sand_pos) > 0)  # Ensure exactly one position is recorded

# Sandpipers in Howard (hall slot = False)
for i in range(5):
    solver.add(Implies(slot[i] == 3, hall[i] == False))

# Sandpipers earlier than oystercatchers
oyst_pos = [Int(f"oyst_pos_{i}") for i in range(5)]
for i in range(5):
    solver.add(oyst_pos[i] == If(slot[i] == 0, i + 1, 0))
solver.add(Sum(oyst_pos) > 0)

# pos(sandpiper) < pos(oystercatcher)
sand_pos_val = Int("sand_pos_val")
oyst_pos_val = Int("oyst_pos_val")
solver.add(And(
    Or([And(slot[i] == 3, sand_pos_val == i + 1) for i in range(5)]),
    Or([And(slot[i] == 0, oyst_pos_val == i + 1) for i in range(5)]),
    sand_pos_val < oyst_pos_val
))

# Tern/petrel constraints
tern_pos = [Int(f"tern_pos_{i}") for i in range(5)]
for i in range(5):
    solver.add(tern_pos[i] == If(slot[i] == 4, i + 1, 0))
solver.add(Sum(tern_pos) > 0)

pet_pos = [Int(f"pet_pos_{i}") for i in range(5)]
for i in range(5):
    solver.add(pet_pos[i] == If(slot[i] == 1, i + 1, 0))
solver.add(Sum(pet_pos) > 0)

# Terns earlier than petrels
tern_pos_val = Int("tern_pos_val")
pet_pos_val = Int("pet_pos_val")
solver.add(And(
    Or([And(slot[i] == 4, tern_pos_val == i + 1) for i in range(5)]),
    Or([And(slot[i] == 1, pet_pos_val == i + 1) for i in range(5)]),
    tern_pos_val < pet_pos_val
))

# Petrels in Gladwyn Hall
for i in range(5):
    solver.add(Implies(slot[i] == 1, hall[i] == True))

# Answer choices (0-indexed positions for hall array)
# A: hall[0] and hall[1] both True
# B: hall[1] and hall[2] both False
# C: hall[1] and hall[4] both True
# D: hall[2] and hall[3] both False
# E: hall[2] and hall[4] both True

answer_conditions = [
    And(hall[0], hall[1]),  # A
    And(Not(hall[1]), Not(hall[2])),  # B
    And(hall[1], hall[4]),  # C
    And(Not(hall[2]), Not(hall[3])),  # D
    And(hall[2], hall[4])   # E
]

answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)