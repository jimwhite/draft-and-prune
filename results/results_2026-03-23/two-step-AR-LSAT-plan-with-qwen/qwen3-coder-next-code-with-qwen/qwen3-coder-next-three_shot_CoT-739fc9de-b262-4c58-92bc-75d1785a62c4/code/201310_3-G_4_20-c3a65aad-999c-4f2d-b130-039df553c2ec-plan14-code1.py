from z3 import *

# Bird types: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
birds = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
pos = [Int(f"pos_{i}") for i in range(5)]  # pos[i] = position of bird type i (1-5)

# Venue variables: hall[i] = True if lecture at position i+1 is in Gladwyn Hall
hall = [Bool(f"hall_{i}") for i in range(5)]

solver = Solver()

# Domain constraints: each bird appears exactly once at positions 1-5
solver.add(Distinct(pos))
for i in range(5):
    solver.add(pos[i] >= 1, pos[i] <= 5)

# Fixed venue constraints
solver.add(hall[0] == True)   # first lecture (position 1) in Gladwyn
solver.add(hall[3] == False)  # fourth lecture (position 4) in Howard

# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[i], 1, 0) for i in range(5)]) == 3)

# Sandpiper constraint: sandpipers (index 3) in Howard, earlier than oystercatchers
sandpiper_pos = pos[3]
solver.add(Not(hall[sandpiper_pos - 1]))

# Use piecewise linearization for hall index: introduce helper variables
sandpiper_idx = Int('sandpiper_idx')
solver.add(sandpiper_idx == sandpiper_pos - 1)
# Enforce that sandpiper_idx is between 0 and 4
solver.add(sandpiper_idx >= 0, sandpiper_idx <= 4)
# Enforce hall[sandpiper_pos - 1] == False using conditional constraints
for i in range(5):
    solver.add(Implies(sandpiper_idx == i, Not(hall[i])))

solver.add(pos[3] < pos[0])

# Terns/petrels constraint: terns (index 4) before petrels (index 1), petrels in Gladwyn
solver.add(pos[4] < pos[1])
petrel_pos = pos[1]
# Enforce hall[petrel_pos - 1] == True using similar linearization
petrel_idx = Int('petrel_idx')
solver.add(petrel_idx == petrel_pos - 1)
solver.add(petrel_idx >= 0, petrel_idx <= 4)
for i in range(5):
    solver.add(Implies(petrel_idx == i, hall[i]))

# Answer choices (0-indexed in the list, but positions are 1-indexed)
answer_choices = [
    # "The first and second lectures are both in Gladwyn Hall."
    And(hall[0] == True, hall[1] == True),
    # "The second and third lectures are both in Howard Auditorium."
    And(hall[1] == False, hall[2] == False),
    # "The second and fifth lectures are both in Gladwyn Hall."
    And(hall[1] == True, hall[4] == True),
    # "The third and fourth lectures are both in Howard Auditorium."
    And(hall[2] == False, hall[3] == False),
    # "The third and fifth lectures are both in Gladwyn Hall."
    And(hall[2] == True, hall[4] == True)
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)