from z3 import *

# Bird indices
(OYSTER, PETREL, RAIL, SAND, TERN) = range(5)

# Hall assignment per lecture slot (0-4): True=Gladwyn, False=Howard
hall = [Bool(f"hall_{i}") for i in range(5)]

# Position variables: pos[bird] = lecture slot (0-4) for that bird
pos = [Int(f"pos_{b}") for b in range(5)]

# Bird hall assignment: bird_hall[b] = True if bird's lecture is in Gladwyn
bird_hall = [Bool(f"bird_hall_{b}") for b in range(5)]

# Base solver
solver = Solver()

# Fixed constraints on hall assignments
solver.add(hall[0] == True)  # First lecture in Gladwyn Hall
solver.add(hall[3] == False) # Fourth lecture in Howard Auditorium
# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[i], 1, 0) for i in range(5)]) == 3)

# All positions distinct (each bird has unique slot)
solver.add(Distinct(pos))

# Each position between 0 and 4
for p in pos:
    solver.add(p >= 0, p <= 4)

# Link bird_hall to hall via position: for each bird b, bird_hall[b] == hall[pos[b]]
# Since positions are bijective, we can use: for each slot i and bird b,
# if pos[b] == i then bird_hall[b] == hall[i]
for b in range(5):
    # Build equivalence: bird_hall[b] == hall[pos[b]]
    # Using big conjunction of implications for each possible position
    constraints = []
    for i in range(5):
        constraints.append(Implies(pos[b] == i, bird_hall[b] == hall[i]))
    solver.add(And(constraints))

# Sandpiper constraint: in Howard (False) and earlier than oystercatcher
solver.add(bird_hall[SAND] == False)
solver.add(pos[SAND] < pos[OYSTER])

# Tern constraint: earlier than petrel, and petrel in Gladwyn
solver.add(pos[TERN] < pos[PETREL])
solver.add(bird_hall[PETREL] == True)

# Answer choices: each is a condition about hall assignments at specific slots
answer_conditions = [
    And(hall[0], hall[1]),  # First and second both Gladwyn
    And(Not(hall[1]), Not(hall[2])),  # Second and third both Howard (i.e., not Gladwyn)
    And(hall[1], hall[4]),  # Second and fifth both Gladwyn
    And(Not(hall[2]), Not(hall[3])),  # Third and fourth both Howard
    And(hall[2], hall[4])   # Third and fifth both Gladwyn
]

# Check each choice: if UNSAT when condition is asserted, then it must be false
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(cond)
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Since exactly one must be false, output the index
print(answer_index_list[0] if answer_index_list else -1)