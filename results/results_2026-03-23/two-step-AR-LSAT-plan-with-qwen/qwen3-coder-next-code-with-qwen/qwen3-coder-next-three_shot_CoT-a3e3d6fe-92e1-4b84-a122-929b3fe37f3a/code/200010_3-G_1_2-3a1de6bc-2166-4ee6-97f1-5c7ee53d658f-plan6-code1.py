from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
n_students = 8

# Boolean variables
assigned = [Bool(f"assigned_{i}") for i in range(n_students)]
# day[i][d]: student i gives report on day d (0=Mon, 1=Tue, 2=Wed)
day = [[Bool(f"day_{i}_{d}") for d in range(3)] for i in range(n_students)]
# slot[i][s]: student i gives report in slot s (0=morning, 1=afternoon)
slot = [[Bool(f"slot_{i}_{s}") for s in range(2)] for i in range(n_students)]

# Base solver
solver = Solver()

# Exactly 6 students give reports
solver.add(Sum([If(assigned[i], 1, 0) for i in range(n_students)]) == 6)

# Each student gives at most one report (if assigned, exactly one day and slot)
for i in range(n_students):
    # If assigned, must have exactly one day
    solver.add(Implies(assigned[i], Sum([If(day[i][d], 1, 0) for d in range(3)]) == 1))
    # If assigned, must have exactly one slot
    solver.add(Implies(assigned[i], Sum([If(slot[i][s], 1, 0) for s in range(2)]) == 1))
    # If not assigned, no day or slot
    solver.add(Implies(Not(assigned[i]), And(*[Not(day[i][d]) for d in range(3)])))
    solver.add(Implies(Not(assigned[i]), And(*[Not(slot[i][s]) for s in range(2)])))

# Each day has exactly two reports
for d in range(3):
    solver.add(Sum([If(day[i][d], 1, 0) for i in range(n_students)]) == 2)

# George can only give report on Tuesday
solver.add(Not(assigned[0]) | day[0][1])
solver.add(Not(day[0][0]))
solver.add(Not(day[0][2]))

# Olivia and Robert cannot give afternoon reports
solver.add(Not(slot[6][1]))  # Olivia
solver.add(Not(slot[7][1]))  # Robert

# Nina conditional constraint
nina_mon = day[5][0]
nina_tue = day[5][1]
nina_wed = day[5][2]

# If Nina reports on Monday, then Helen and Irving must report Tuesday
solver.add(Implies(nina_mon, And(day[1][1], day[2][1])))
# If Nina reports on Tuesday, then Helen and Irving must report Wednesday
solver.add(Implies(nina_tue, And(day[1][2], day[2][2])))
# If Nina reports on Wednesday, no constraint
solver.add(Implies(nina_wed, True))

# Kyle and Lenore do not give reports
solver.add(Not(assigned[3]))  # Kyle
solver.add(Not(assigned[4]))  # Lenore

# Answer choices: list of (mon_morning, tue_morning, wed_morning) student indices
answer_choices = [
    (1, 0, 5),  # Helen, George, Nina
    (2, 7, 1),  # Irving, Robert, Helen
    (5, 1, 6),  # Nina, Helen, Olivia
    (6, 7, 2),  # Olivia, Robert, Irving
    (7, 0, 1)   # Robert, George, Helen
]

# Check each answer choice
answer_index_list = []
for idx, (mon_mor, tue_mor, wed_mor) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for the specific answer choice
    # Each specified student must be assigned and in the correct slot/day
    # Monday morning: mon_mor
    s_chk.add(assigned[mon_mor])
    s_chk.add(day[mon_mor][0])
    s_chk.add(slot[mon_mor][0])
    
    # Tuesday morning: tue_mor
    s_chk.add(assigned[tue_mor])
    s_chk.add(day[tue_mor][1])
    s_chk.add(slot[tue_mor][0])
    
    # Wednesday morning: wed_mor
    s_chk.add(assigned[wed_mor])
    s_chk.add(day[wed_mor][2])
    s_chk.add(slot[wed_mor][0])
    
    # Ensure no other student is assigned to the same slot/day
    for i in range(n_students):
        if i != mon_mor:
            s_chk.add(Implies(day[i][0], Not(slot[i][0])))
        if i != tue_mor:
            s_chk.add(Implies(day[i][1], Not(slot[i][0])))
        if i != wed_mor:
            s_chk.add(Implies(day[i][2], Not(slot[i][0])))
    
    # Ensure exactly 6 students are assigned (already in base solver, but we add explicit constraints for the three)
    # The solver already enforces exactly 6 assigned, so no need to add more
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)