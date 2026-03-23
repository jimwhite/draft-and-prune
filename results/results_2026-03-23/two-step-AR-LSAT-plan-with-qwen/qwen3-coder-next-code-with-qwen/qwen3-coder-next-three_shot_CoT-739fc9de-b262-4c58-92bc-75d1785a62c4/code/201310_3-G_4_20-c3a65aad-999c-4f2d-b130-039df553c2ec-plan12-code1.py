from z3 import *

# Bird types: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
birds = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
pos = {bird: Int(f"pos_{bird}") for bird in birds}

# Hall assignments: hall[i] = True if lecture at position i+1 is in Gladwyn Hall
hall = [Bool(f"hall_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Hall constraints
solver.add(hall[0] == True)  # First lecture in Gladwyn Hall
solver.add(hall[3] == False) # Fourth lecture in Howard Auditorium

# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[i], 1, 0) for i in range(5)]) == 3)

# Bird position constraints
solver.add(Distinct(*pos.values()))
for bird in birds:
    solver.add(pos[bird] >= 1, pos[bird] <= 5)

# Sandpiper constraint: in Howard Auditorium and earlier than oystercatchers
sandpiper_hall = If(pos["sandpipers"] == 1, hall[0],
           If(pos["sandpipers"] == 2, hall[1],
           If(pos["sandpipers"] == 3, hall[2],
           If(pos["sandpipers"] == 4, hall[3], hall[4]))))
solver.add(sandpiper_hall == False)
solver.add(pos["sandpipers"] < pos["oystercatchers"])

# Tern-petrel constraint: terns earlier than petrels, and petrels in Gladwyn Hall
solver.add(pos["terns"] < pos["petrels"])
petrel_hall = If(pos["petrels"] == 1, hall[0],
           If(pos["petrels"] == 2, hall[1],
           If(pos["petrels"] == 3, hall[2],
           If(pos["petrels"] == 4, hall[3], hall[4]))))
solver.add(petrel_hall == True)

# Answer choices (each is a condition that must be checked for falsity)
answer_choices = [
    And(hall[0], hall[1]),  # First and second in Gladwyn
    And(Not(hall[1]), Not(hall[2])),  # Second and third in Howard
    And(hall[1], hall[4]),  # Second and fifth in Gladwyn
    And(Not(hall[2]), Not(hall[3])),  # Third and fourth in Howard
    And(hall[2], hall[4])   # Third and fifth in Gladwyn
]

# Check each answer choice
answer_index_list = []
for idx, condition in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(condition)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)