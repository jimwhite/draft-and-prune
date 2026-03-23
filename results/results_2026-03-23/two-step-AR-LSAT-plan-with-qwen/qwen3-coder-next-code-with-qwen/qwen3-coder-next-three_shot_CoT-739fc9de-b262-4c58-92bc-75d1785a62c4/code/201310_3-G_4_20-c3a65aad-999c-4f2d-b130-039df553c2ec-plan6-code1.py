from z3 import *

# Bird types: 0-oystercatchers, 1-petrels, 2-rails, 3-sandpipers, 4-terns
birds = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
pos = [Int(f"pos_{bird}") for bird in birds]

# Hall variables: hall[i] = True if lecture at position i+1 is in Gladwyn Hall
hall = [Bool(f"hall_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Position constraints: each bird has a distinct position from 1 to 5
solver.add(Distinct(*pos))
for p in pos:
    solver.add(p >= 1, p <= 5)

# Hall constraints
solver.add(hall[0] == True)  # First lecture in Gladwyn Hall
solver.add(hall[3] == False) # Fourth lecture in Howard Auditorium
solver.add(Sum([If(hall[i], 1, 0) for i in range(5)]) == 3) # Exactly three Gladwyn Hall lectures

# Sandpiper constraints
sandpipers_idx = 3
solver.add(If(pos[sandpipers_idx] == 1, hall[0], 
              If(pos[sandpipers_idx] == 2, hall[1],
                 If(pos[sandpipers_idx] == 3, hall[2],
                    If(pos[sandpipers_idx] == 4, hall[3], hall[4]))) == False) # Sandpipers in Howard Auditorium
solver.add(pos[sandpipers_idx] < pos[0]) # Sandpipers before oystercatchers

# Terns and petrels constraints
terns_idx = 4
petrels_idx = 1
solver.add(pos[terns_idx] < pos[petrels_idx]) # Terns before petrels
solver.add(If(pos[petrels_idx] == 1, hall[0],
              If(pos[petrels_idx] == 2, hall[1],
                 If(pos[petrels_idx] == 3, hall[2],
                    If(pos[petrels_idx] == 4, hall[3], hall[4]))) == True) # Petrels in Gladwyn Hall

# Answer choices (each is a conjunction of hall constraints)
answer_choices = [
    And(hall[0] == True, hall[1] == True),  # First and second in Gladwyn Hall
    And(hall[1] == False, hall[2] == False), # Second and third in Howard Auditorium
    And(hall[0] == True, hall[4] == True),   # First and fifth in Gladwyn Hall
    And(hall[2] == False, hall[3] == False), # Third and fourth in Howard Auditorium
    And(hall[2] == True, hall[4] == True)    # Third and fifth in Gladwyn Hall
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)