from z3 import *

# Lecture positions: 1 to 5 (using 0-indexed internally, so position i corresponds to index i-1)
# Bird types: oystercatchers, petrels, rails, sandpipers, terns
birds = ["oystercatchers", "petrels", "rails", "sandpipers", "terns"]
bird_vars = [Int(f"slot_{b}") for b in birds]

# Location variables: Gladwyn Hall = True, Howard Auditorium = False
# Using 0-indexed positions: position 0 = slot 1, ..., position 4 = slot 5
Gladwyn = [Bool(f"Gladwyn_{i}") for i in range(5)]

# Base solver
solver = Solver()

# All bird slots are distinct and between 1 and 5 (0-indexed: 0 to 4)
solver.add(Distinct(bird_vars))
for bv in bird_vars:
    solver.add(bv >= 0, bv <= 4)

# Fixed location constraints
# First lecture (position 0) is in Gladwyn Hall
solver.add(Gladwyn[0] == True)
# Fourth lecture (position 3) is in Howard Auditorium
solver.add(Gladwyn[3] == False)
# Exactly three lectures are in Gladwyn Hall
solver.add(Sum([If(Gladwyn[i], 1, 0) for i in range(5)]) == 3)

# Sandpiper constraints
sandpiper_idx = birds.index("sandpipers")
oystercatcher_idx = birds.index("oystercatchers")

# Sandpipers lecture is in Howard Auditorium
sandpiper_pos = bird_vars[sandpiper_idx]
solver.add(If(sandpiper_pos == 0, False,
              If(sandpiper_pos == 1, False,
                 If(sandpiper_pos == 2, False,
                    If(sandpiper_pos == 3, False,
                       If(sandpiper_pos == 4, False, True))))))

# Sandpipers lecture occurs before oystercatchers
solver.add(bird_vars[sandpiper_idx] < bird_vars[oystercatcher_idx])

# Tern-petrel constraints
tern_idx = birds.index("terns")
petrel_idx = birds.index("petrels")

# Petrels lecture is in Gladwyn Hall
petrel_pos = bird_vars[petrel_idx]
solver.add(If(petrel_pos == 0, True,
              If(petrel_pos == 1, True,
                 If(petrel_pos == 2, True,
                    If(petrel_pos == 3, False,
                       If(petrel_pos == 4, True, True))))))

# Terns lecture occurs before petrels
solver.add(bird_vars[tern_idx] < bird_vars[petrel_idx])

# Answer choices (each is a pair of positions that are both in Gladwyn Hall)
# Using 1-indexed positions from the question, convert to 0-indexed:
# Choice 0: first and second lectures (positions 0,1)
# Choice 1: second and third lectures (positions 1,2)
# Choice 2: second and fifth lectures (positions 1,4)
# Choice 3: third and fourth lectures (positions 2,3)
# Choice 4: third and fifth lectures (positions 2,4)

answer_choices = [
    (0, 1),  # first and second
    (1, 2),  # second and third
    (1, 4),  # second and fifth
    (2, 3),  # third and fourth
    (2, 4)   # third and fifth
]

# Check each answer choice
answer_index_list = []
for idx, (pos1, pos2) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert both positions are in Gladwyn Hall
    s_chk.add(Gladwyn[pos1] == True, Gladwyn[pos2] == True)
    
    # If UNSAT, this choice must be false
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)