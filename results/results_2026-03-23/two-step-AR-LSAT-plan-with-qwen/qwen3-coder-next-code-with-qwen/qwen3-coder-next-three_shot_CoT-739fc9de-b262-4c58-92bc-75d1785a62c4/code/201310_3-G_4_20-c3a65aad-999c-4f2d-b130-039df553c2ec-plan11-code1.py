from z3 import *

# Bird types: 0-oystercatchers, 1-petrels, 2-rails, 3-sandpipers, 4-terns
BIRDS = range(5)

# Location variables: loc[i] = True means Gladwyn Hall, False means Howard Auditorium
loc = [Bool(f"loc_{i}") for i in range(5)]

# Bird assignment variables: bird[i] = type of bird in slot i (0-4)
bird = [Int(f"bird_{i}") for i in range(5)]

# Slot index variables
sand_slot = Int("sand_slot")
oys_slot = Int("oys_slot")
tern_slot = Int("tern_slot")
pet_slot = Int("pet_slot")

# Base solver
solver = Solver()

# Location constraints
## Slot 1 (index 0) is Gladwyn Hall (True)
solver.add(loc[0] == True)
## Slot 4 (index 3) is Howard Auditorium (False)
solver.add(loc[3] == False)
## Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(loc[i], 1, 0) for i in range(5)]) == 3)

# Bird type constraints
## All bird types used exactly once
solver.add(Distinct(bird))

# Assign each slot a valid bird type (0-4)
for i in range(5):
    solver.add(Or([bird[i] == b for b in BIRDS]))

# Sandpipers constraints
## Sandpipers lecture is in Howard Auditorium (False)
solver.add(And(0 <= sand_slot, sand_slot < 5))
solver.add(bird[sand_slot] == 3)  # sandpipers = 3
solver.add(loc[sand_slot] == False)

# Sandpipers earlier than oystercatchers
solver.add(And(0 <= oys_slot, oys_slot < 5))
solver.add(bird[oys_slot] == 0)  # oystercatchers = 0
solver.add(sand_slot < oys_slot)

# Terns and petrels constraints
solver.add(And(0 <= tern_slot, tern_slot < 5))
solver.add(bird[tern_slot] == 4)  # terns = 4

solver.add(And(0 <= pet_slot, pet_slot < 5))
solver.add(bird[pet_slot] == 1)  # petrels = 1

# Terns earlier than petrels
solver.add(tern_slot < pet_slot)

# Petrels in Gladwyn Hall (True)
solver.add(loc[pet_slot] == True)

# Answer choices: each is a condition that we test for consistency
# If the condition leads to UNSAT, then it must be false (i.e., cannot happen)
answer_choices = [
    # 0: First and second lectures both in Gladwyn Hall → loc[0] ∧ loc[1]
    lambda: And(loc[0], loc[1]),
    # 1: Second and third lectures both in Howard Auditorium → ¬loc[1] ∧ ¬loc[2]
    lambda: And(Not(loc[1]), Not(loc[2])),
    # 2: Second and fifth lectures both in Gladwyn Hall → loc[1] ∧ loc[4]
    lambda: And(loc[1], loc[4]),
    # 3: Third and fourth lectures both in Howard Auditorium → ¬loc[2] ∧ ¬loc[3]
    lambda: And(Not(loc[2]), Not(loc[3])),
    # 4: Third and fifth lectures both in Gladwyn Hall → loc[2] ∧ loc[4]
    lambda: And(loc[2], loc[4])
]

answer_index_list = []
for idx, choice_cond in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the condition from the answer choice
    s_chk.add(choice_cond())
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)