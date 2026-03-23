from z3 import *

# Bird types: 0-oystercatchers, 1-petrels, 2-rails, 3-sandpipers, 4-terns
BIRDS = range(5)

# Position variables: bird_order[i] = bird type at position i (0-indexed)
bird_order = [Int(f"bird_{i}") for i in range(5)]

# Hall variables: hall[i] = True if lecture at position i is in Gladwyn Hall, False for Howard
hall = [Bool(f"hall_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Domain constraints: each bird appears exactly once
solver.add(Distinct(bird_order))
for i in range(5):
    solver.add(And(bird_order[i] >= 0, bird_order[i] <= 4))

# Venue constraints
solver.add(hall[0] == True)  # First lecture in Gladwyn Hall
solver.add(hall[3] == False)  # Fourth lecture in Howard Auditorium
# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[i], 1, 0) for i in range(5)]) == 3)

# Find positions of specific birds
pos = {}
for bird in BIRDS:
    # Create position variable for each bird type
    pos[bird] = Int(f"pos_{bird}")
    # Position must be between 0 and 4
    solver.add(pos[bird] >= 0, pos[bird] <= 4)
    # Position matches bird_order: if bird_order[i] == bird, then pos[bird] = i
    # Use equivalence: pos[bird] == i iff bird_order[i] == bird
    for i in range(5):
        solver.add(Implies(bird_order[i] == bird, pos[bird] == i))
        solver.add(Implies(pos[bird] == i, bird_order[i] == bird))

# Sandpiper constraint: in Howard Auditorium and earlier than oystercatchers
# Use piecewise definition for hall[pos[3]] since pos[3] is a variable
hall_sandpiper = [If(pos[3] == i, hall[i], BoolVal(False)) for i in range(5)]
solver.add(Sum(hall_sandpiper) == 0)  # hall[pos[3]] must be False
solver.add(pos[3] < pos[0])           # sandpipers before oystercatchers

# Tern-petrel constraint: terns earlier than petrels, petrels in Gladwyn
solver.add(pos[4] < pos[1])           # terns before petrels
# Use piecewise definition for hall[pos[1]]
hall_petrel = [If(pos[1] == i, hall[i], BoolVal(False)) for i in range(5)]
solver.add(Sum(hall_petrel) == 1)     # hall[pos[1]] must be True

# Answer choices (as venue conditions)
answer_conditions = [
    And(hall[0], hall[1]),  # A: first and second in Gladwyn
    And(Not(hall[1]), Not(hall[2])),  # B: second and third in Howard
    And(hall[1], hall[4]),  # C: second and fifth in Gladwyn
    And(Not(hall[2]), Not(hall[3])),  # D: third and fourth in Howard
    And(hall[2], hall[4])   # E: third and fifth in Gladwyn
]

# Check each answer choice
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)