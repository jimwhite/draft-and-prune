from z3 import *

# Bird types indices: 0-oystercatchers, 1-petrels, 2-rails, 3-sandpipers, 4-terns
(OYS, PET, RAIL, SAND, TERN) = range(5)

# Hall assignment variables: G[i] = True if lecture i (1-indexed) is in Gladwyn Hall
G = [Bool(f"G_{i}") for i in range(6)]  # index 0 unused, use 1-5

# Bird assignment variables: bird[i] = bird type for lecture i (1-indexed)
bird = [Int(f"bird_{i}") for i in range(6)]  # index 0 unused

# Position variables: pos[t] = position where bird type t occurs (1-indexed)
pos = [Int(f"pos_{t}") for t in range(5)]

# Base solver
solver = Solver()

# Hall constraints
## First lecture in Gladwyn Hall
solver.add(G[1] == True)
## Fourth lecture in Howard Auditorium (not Gladwyn Hall)
solver.add(G[4] == False)
## Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(G[i], 1, 0) for i in range(1, 6)]) == 3)

# Bird constraints
## Each lecture has a distinct bird type (0-4)
for i in range(1, 6):
    solver.add(And(bird[i] >= OYS, bird[i] <= TERN))

# Ensure each bird type appears exactly once
solver.add(Distinct([bird[i] for i in range(1, 6)]))

# Link bird assignments to positions: pos[t] = i iff bird[i] = t
for t in range(5):
    solver.add(pos[t] == If(bird[1] == t, 1,
                   If(bird[2] == t, 2,
                   If(bird[3] == t, 3,
                   If(bird[4] == t, 4,
                   If(bird[5] == t, 5, 0))))))

# Sandpipers constraint: in Howard Auditorium and earlier than oystercatchers
solver.add(G[pos[SAND]] == False)  # Howard Auditorium
solver.add(pos[SAND] < pos[OYS])

# Terns and petrels constraint: terns before petrels, petrels in Gladwyn Hall
solver.add(pos[TERN] < pos[PET])
solver.add(G[pos[PET]] == True)  # Gladwyn Hall

# Answer choices (each is a scenario to test)
answer_choices = [
    # A: First and second lectures are both in Gladwyn Hall
    lambda: And(G[1] == True, G[2] == True),
    # B: Second and third lectures are both in Howard Auditorium
    lambda: And(G[2] == False, G[3] == False),
    # C: Second and fifth lectures are both in Gladwyn Hall
    lambda: And(G[2] == True, G[5] == True),
    # D: Third and fourth lectures are both in Howard Auditorium
    lambda: And(G[3] == False, G[4] == False),
    # E: Third and fifth lectures are both in Gladwyn Hall
    lambda: And(G[3] == True, G[5] == True)
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    # Add the scenario condition
    s_chk.add(choice())
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)