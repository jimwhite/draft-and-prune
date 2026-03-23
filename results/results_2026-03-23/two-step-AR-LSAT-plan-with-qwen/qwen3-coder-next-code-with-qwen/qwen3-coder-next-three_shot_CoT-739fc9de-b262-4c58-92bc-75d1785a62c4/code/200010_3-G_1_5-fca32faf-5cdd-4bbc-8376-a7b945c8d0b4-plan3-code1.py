from z3 import *

# Student indices: George=0, Helen=1, Irving=2, Kyle=3, Lenore=4, Nina=5, Olivia=6, Robert=7
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]
student_idx = {s: i for i, s in enumerate(students)}

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
days = range(3)

# Variables: Morning[d][s] and Afternoon[d][s] are Booleans
Morning = [[Bool(f"Morning_{d}_{s}") for s in range(8)] for d in days]
Afternoon = [[Bool(f"Afternoon_{d}_{s}") for s in range(8)] for d in days]

solver = Solver()

# Exactly six reports total
reports = []
for d in days:
    for s in range(8):
        reports.append(Morning[d][s])
        reports.append(Afternoon[d][s])
solver.add(Sum([If(r, 1, 0) for r in reports]) == 6)

# One report per time slot each day
for d in days:
    solver.add(Sum([If(Morning[d][s], 1, 0) for s in range(8)]) == 1)
    solver.add(Sum([If(Afternoon[d][s], 1, 0) for s in range(8)]) == 1)

# No student reports more than once
for s in range(8):
    assignments = []
    for d in days:
        assignments.append(Morning[d][s])
        assignments.append(Afternoon[d][s])
    solver.add(Sum([If(a, 1, 0) for a in assignments]) <= 1)

# Tuesday is the only day George can give a report
for d in days:
    if d != 1:  # not Tuesday
        solver.add(Not(Morning[d][student_idx["George"]]))
        solver.add(Not(Afternoon[d][student_idx["George"]]))

# Olivia and Robert cannot give afternoon reports
for s in [student_idx["Olivia"], student_idx["Robert"]]:
    for d in days:
        solver.add(Not(Afternoon[d][s]))

# Nina conditional constraint
nina_mon = Or(Morning[0][student_idx["Nina"]], Afternoon[0][student_idx["Nina"]])
nina_tue = Or(Morning[1][student_idx["Nina"]], Afternoon[1][student_idx["Nina"]])
nina_wed = Or(Morning[2][student_idx["Nina"]], Afternoon[2][student_idx["Nina"]])

# If Nina reports on Monday, then Helen and Irving must both report on Tuesday
solver.add(Implies(nina_mon, 
    And(
        Or(Morning[1][student_idx["Helen"]], Afternoon[1][student_idx["Helen"]]), 
        Or(Morning[1][student_idx["Irving"]], Afternoon[1][student_idx["Irving"]])
    )))

# If Nina reports on Tuesday, then Helen and Irving must both report on Wednesday
solver.add(Implies(nina_tue,
    And(
        Or(Morning[2][student_idx["Helen"]], Afternoon[2][student_idx["Helen"]]), 
        Or(Morning[2][student_idx["Irving"]], Afternoon[2][student_idx["Irving"]])
    )))

# If Nina reports on Wednesday, no constraint (vacuously satisfied)

# Given assumptions
solver.add(Afternoon[1][student_idx["Kyle"]] == True)  # Kyle gives afternoon report on Tuesday
solver.add(Afternoon[2][student_idx["Helen"]] == True)  # Helen gives afternoon report on Wednesday

# Answer choices: morning reports for Mon, Tue, Wed
answer_choices = [
    ["Irving", "Lenore", "Nina"],
    ["Lenore", "George", "Irving"],
    ["Nina", "Irving", "Lenore"],
    ["Robert", "George", "Irving"],
    ["Robert", "Irving", "Lenore"]
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add morning report assignments for the choice
    mon_morning = student_idx[choice[0]]
    tue_morning = student_idx[choice[1]]
    wed_morning = student_idx[choice[2]]
    
    s_chk.add(Morning[0][mon_morning] == True)
    s_chk.add(Morning[1][tue_morning] == True)
    s_chk.add(Morning[2][wed_morning] == True)
    
    # Ensure no other assignments for these students on those days
    for s in [mon_morning, tue_morning, wed_morning]:
        # Morning assignments already set for specific days
        if s == mon_morning:
            for d in days:
                if d != 0:
                    s_chk.add(Not(Morning[d][s]))
                    s_chk.add(Not(Afternoon[d][s]))
        if s == tue_morning:
            for d in days:
                if d != 1:
                    s_chk.add(Not(Morning[d][s]))
                    s_chk.add(Not(Afternoon[d][s]))
        if s == wed_morning:
            for d in days:
                if d != 2:
                    s_chk.add(Not(Morning[d][s]))
                    s_chk.add(Not(Afternoon[d][s]))
    
    # Also ensure Kyle and Helen are only assigned where specified
    s_chk.add(Afternoon[1][student_idx["Kyle"]] == True)
    s_chk.add(Not(Morning[1][student_idx["Kyle"]]))
    for d in days:
        if d != 1:
            s_chk.add(Not(Morning[d][student_idx["Kyle"]]))
            s_chk.add(Not(Afternoon[d][student_idx["Kyle"]]))
    
    s_chk.add(Afternoon[2][student_idx["Helen"]] == True)
    s_chk.add(Not(Morning[2][student_idx["Helen"]]))
    for d in days:
        if d != 2:
            s_chk.add(Not(Morning[d][student_idx["Helen"]]))
            s_chk.add(Not(Afternoon[d][student_idx["Helen"]]))
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)