from z3 import *

# Bird types: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
birds = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
pos = [Int(f"pos_{i}") for i in range(5)]

# hall[i] = 1 if lecture at position i+1 is in Gladwyn Hall, 0 otherwise
hall = [Int(f"hall_{i}") for i in range(5)]

solver = Solver()

# Domain constraints: each bird has unique position from 1 to 5
for i in range(5):
    solver.add(pos[i] >= 1, pos[i] <= 5)
solver.add(Distinct(*pos))

# Hall constraints
for i in range(5):
    solver.add(hall[i] == 1, hall[i] <= 1)  # Boolean: 0 or 1

# Fixed location constraints
solver.add(hall[0] == 1)  # First lecture in Gladwyn Hall
solver.add(hall[3] == 0)  # Fourth lecture in Howard Auditorium

# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[i] == 1, 1, 0) for i in range(5)]) == 3)

# Sandpipers constraints
sandpiper_pos = pos[3]
solver.add(And(sandpiper_pos >= 1, sandpiper_pos <= 5))
solver.add(If(sandpiper_pos == 1, hall[0] == 0,
              If(sandpiper_pos == 2, hall[1] == 0,
                 If(sandpiper_pos == 3, hall[2] == 0,
                    If(sandpiper_pos == 4, hall[3] == 0,
                       If(sandpiper_pos == 5, hall[4] == 0, True))))) == True)
solver.add(pos[3] < pos[0])       # Sandpipers before oystercatchers

# Terns and petrels constraints
solver.add(pos[4] < pos[1])       # Terns before petrels
petrel_pos = pos[1]
solver.add(And(petrel_pos >= 1, petrel_pos <= 5))
solver.add(If(petrel_pos == 1, hall[0] == 1,
              If(petrel_pos == 2, hall[1] == 1,
                 If(petrel_pos == 3, hall[2] == 1,
                    If(petrel_pos == 4, hall[3] == 1,
                       If(petrel_pos == 5, hall[4] == 1, True))))) == True)

# Answer choices (each is a pair of positions that must both be in the same hall)
# 0: first and second (positions 1,2) both Gladwyn
# 1: second and third (positions 2,3) both Howard
# 2: second and fifth (positions 2,5) both Gladwyn
# 3: third and fourth (positions 3,4) both Howard
# 4: third and fifth (positions 3,5) both Gladwyn

answer_index_list = []
for idx in range(5):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if idx == 0:  # first and second both Gladwyn
        s_chk.add(hall[0] == 1, hall[1] == 1)
    elif idx == 1:  # second and third both Howard
        s_chk.add(hall[1] == 0, hall[2] == 0)
    elif idx == 2:  # second and fifth both Gladwyn
        s_chk.add(hall[1] == 1, hall[4] == 1)
    elif idx == 3:  # third and fourth both Howard
        s_chk.add(hall[2] == 0, hall[3] == 0)
    elif idx == 4:  # third and fifth both Gladwyn
        s_chk.add(hall[2] == 1, hall[4] == 1)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)