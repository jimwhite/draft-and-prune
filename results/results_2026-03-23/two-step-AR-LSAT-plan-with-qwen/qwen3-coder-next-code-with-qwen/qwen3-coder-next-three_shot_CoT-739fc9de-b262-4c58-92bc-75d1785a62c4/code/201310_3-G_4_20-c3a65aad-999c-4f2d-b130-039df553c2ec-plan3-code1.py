from z3 import *

# Bird types: 0=oystercatchers, 1=petrels, 2=rails, 3=sandpipers, 4=terns
bird = [Int(f"bird_{i}") for i in range(1, 6)]  # bird[i] = bird type at slot i (1-indexed)

# Hall assignments: True=Gladwyn, False=Howard
hall = [Bool(f"hall_{i}") for i in range(1, 6)]  # hall[i-1] corresponds to slot i

# Base solver
solver = Solver()

# Domain constraints: each bird type appears exactly once (1-5)
solver.add(Distinct(bird))
for i in range(5):
    solver.add(bird[i] >= 0, bird[i] <= 4)

# Hall constraints
solver.add(hall[0] == True)      # first lecture in Gladwyn Hall
solver.add(hall[3] == False)     # fourth lecture in Howard Auditorium

# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(hall[i], 1, 0) for i in range(5)]) == 3)

# Sandpipers constraints
# Find position of sandpipers (bird type 3)
sand_pos = Int('sand_pos')
solver.add(And(sand_pos >= 1, sand_pos <= 5))
for i in range(5):
    solver.add(Implies(bird[i] == 3, (i + 1) == sand_pos))
# Sandpipers in Howard Auditorium
solver.add(Not(If(sand_pos == 1, hall[0],
                 If(sand_pos == 2, hall[1],
                    If(sand_pos == 3, hall[2],
                       If(sand_pos == 4, hall[3], hall[4]))))))

# Oystercatchers position
oc_pos = Int('oc_pos')
solver.add(And(oc_pos >= 1, oc_pos <= 5))
for i in range(5):
    solver.add(Implies(bird[i] == 0, (i + 1) == oc_pos))
# Sandpipers before oystercatchers
solver.add(sand_pos < oc_pos)

# Petrels in Gladwyn Hall
pet_pos = Int('pet_pos')
solver.add(And(pet_pos >= 1, pet_pos <= 5))
for i in range(5):
    solver.add(Implies(bird[i] == 1, (i + 1) == pet_pos))
solver.add(If(pet_pos == 1, hall[0],
             If(pet_pos == 2, hall[1],
                If(pet_pos == 3, hall[2],
                   If(pet_pos == 4, hall[3], hall[4])))))

# Terns before petrels
tern_pos = Int('tern_pos')
solver.add(And(tern_pos >= 1, tern_pos <= 5))
for i in range(5):
    solver.add(Implies(bird[i] == 4, (i + 1) == tern_pos))
solver.add(tern_pos < pet_pos)

# Answer choices (0-indexed)
answer_choices = [
    # C0: first and second lectures both in Gladwyn Hall
    lambda h: And(h[0], h[1]),
    # C1: second and third lectures both in Howard Auditorium
    lambda h: And(Not(h[1]), Not(h[2])),
    # C2: second and fifth lectures both in Gladwyn Hall
    lambda h: And(h[1], h[4]),
    # C3: third and fourth lectures both in Howard Auditorium
    lambda h: And(Not(h[2]), Not(h[3])),
    # C4: third and fifth lectures both in Gladwyn Hall
    lambda h: And(h[2], h[4])
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint for this choice
    s_chk.add(choice(hall))
    
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)