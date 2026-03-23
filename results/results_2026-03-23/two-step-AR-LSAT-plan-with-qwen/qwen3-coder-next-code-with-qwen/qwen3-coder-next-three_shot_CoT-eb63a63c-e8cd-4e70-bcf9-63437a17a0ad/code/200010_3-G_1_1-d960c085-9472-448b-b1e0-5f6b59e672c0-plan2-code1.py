from z3 import *

# Student indices
(STUDENTS, idx_map) = (["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"], {})
for i, s in enumerate(STUDENTS):
    idx_map[s] = i

# Days: 0=Mon, 1=Tue, 2=Wed; Slots: 0=morning, 1=afternoon
report = [[[Bool(f"report_{s}_{d}_{sl}") for sl in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reports total
solver.add(Sum([If(report[s][d][sl], 1, 0) 
                for s in range(8) for d in range(3) for sl in range(2)]) == 6)

# Exactly two reports per day
for d in range(3):
    solver.add(Sum([report[s][d][sl] for s in range(8) for sl in range(2)]) == 2)

# At most one student per slot
for d in range(3):
    for sl in range(2):
        # Exactly one student per slot (since exactly 2 reports per day and only 2 slots)
        solver.add(Sum([report[s][d][sl] for s in range(8)]) == 1)

# George can only report on Tuesday
for sl in range(2):
    solver.add(Not(report[idx_map["George"]][0][sl]))  # Monday
    solver.add(Not(report[idx_map["George"]][2][sl]))  # Wednesday

# Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver.add(Not(report[idx_map["Olivia"]][d][1]))
    solver.add(Not(report[idx_map["Robert"]][d][1]))

# Nina implication constraint
nina_mon = report[idx_map["Nina"]][0][0] | report[idx_map["Nina"]][0][1]
nina_tue = report[idx_map["Nina"]][1][0] | report[idx_map["Nina"]][1][1]
nina_wed = report[idx_map["Nina"]][2][0] | report[idx_map["Nina"]][2][1]

# If Nina on Monday, then Helen and Irving must both report on Tuesday
solver.add(Implies(nina_mon, 
                   And(report[idx_map["Helen"]][1][0] | report[idx_map["Helen"]][1][1],
                       report[idx_map["Irving"]][1][0] | report[idx_map["Irving"]][1][1])))

# If Nina on Tuesday, then Helen and Irving must both report on Wednesday
solver.add(Implies(nina_tue,
                   And(report[idx_map["Helen"]][2][0] | report[idx_map["Helen"]][2][1],
                       report[idx_map["Irving"]][2][0] | report[idx_map["Irving"]][2][1])))

# If Nina on Wednesday, no constraint (already handled by implication logic)

# Answer choices
choices = [
    # Choice 0: 'Mon. morning: Helen; Mon. afternoon: Robert Tues. morning: Olivia; Tues. afternoon: Irving Wed. morning: Lenore; Wed. afternoon: Kyle'
    {"Mon": [("Helen", "morning"), ("Robert", "afternoon")],
     "Tue": [("Olivia", "morning"), ("Irving", "afternoon")],
     "Wed": [("Lenore", "morning"), ("Kyle", "afternoon")]},
    
    # Choice 1: 'Mon. morning: Irving; Mon. afternoon: Olivia Tues. morning: Helen; Tues. afternoon: Kyle Wed. morning: Nina; Wed. afternoon: Lenore'
    {"Mon": [("Irving", "morning"), ("Olivia", "afternoon")],
     "Tue": [("Helen", "morning"), ("Kyle", "afternoon")],
     "Wed": [("Nina", "morning"), ("Lenore", "afternoon")]},
    
    # Choice 2: 'Mon. morning: Lenore; Mon. afternoon: Helen Tues. morning: George; Tues. afternoon: Kyle Wed. morning: Robert; Wed. afternoon: Irving'
    {"Mon": [("Lenore", "morning"), ("Helen", "afternoon")],
     "Tue": [("George", "morning"), ("Kyle", "afternoon")],
     "Wed": [("Robert", "morning"), ("Irving", "afternoon")]},
    
    # Choice 3: 'Mon. morning: Nina; Mon. afternoon: Helen Tues. morning: Robert; Tues. afternoon: Irving Wed. morning: Olivia; Wed. afternoon: Lenore'
    {"Mon": [("Nina", "morning"), ("Helen", "afternoon")],
     "Tue": [("Robert", "morning"), ("Irving", "afternoon")],
     "Wed": [("Olivia", "morning"), ("Lenore", "afternoon")]},
    
    # Choice 4: 'Mon. morning: Olivia; Mon. afternoon: Nina Tues. morning: Irving; Tues. afternoon: Helen Wed. morning: Kyle; Wed. afternoon: George'
    {"Mon": [("Olivia", "morning"), ("Nina", "afternoon")],
     "Tue": [("Irving", "morning"), ("Helen", "afternoon")],
     "Wed": [("Kyle", "morning"), ("George", "afternoon")]},
]

# Check each choice
valid_indices = []
for idx, schedule in enumerate(choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Build set of assigned students for this schedule
    assigned = set()
    for day_str, slots in schedule.items():
        if day_str == "Mon":
            d = 0
        elif day_str == "Tue":
            d = 1
        else:  # Wed
            d = 2
        
        for student, slot_str in slots:
            if student not in idx_map:
                continue
            s_idx = idx_map[student]
            sl = 0 if slot_str == "morning" else 1
            s_chk.add(report[s_idx][d][sl])
            assigned.add((student, d, sl))
    
    # Ensure exactly 6 reports (already enforced globally)
    # Also ensure no other students report
    for s in range(8):
        for d in range(3):
            for sl in range(2):
                if (STUDENTS[s], d, sl) not in assigned:
                    s_chk.add(Not(report[s][d][sl]))
    
    if s_chk.check() == sat:
        valid_indices.append(idx)

print(valid_indices)