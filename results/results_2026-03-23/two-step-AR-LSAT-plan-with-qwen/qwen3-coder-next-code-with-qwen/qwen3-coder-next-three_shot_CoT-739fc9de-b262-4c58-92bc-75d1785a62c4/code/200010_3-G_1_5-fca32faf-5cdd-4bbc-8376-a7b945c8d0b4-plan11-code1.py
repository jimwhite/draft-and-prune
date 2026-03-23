from z3 import *

# Student indices: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
(GEORGE, HELEN, IRVING, KYLE, LENORE, NINA, OLIVIA, ROBERT) = range(8)

# report[s][d][t]: student s gives a report on day d (0=Mon, 1=Tue, 2=Wed) at slot t (0=morning, 1=afternoon)
report = [[[Bool(f"report_{s}_{d}_{t}") for t in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reports total
solver.add(Sum([If(report[s][d][t], 1, 0) 
                for s in range(8) for d in range(3) for t in range(2)]) == 6)

# Exactly two reports per day
for d in range(3):
    solver.add(Sum([If(report[s][d][t], 1, 0) 
                    for s in range(8) for t in range(2)]) == 2)

# One report per slot (at most one student per day/slot)
for d in range(3):
    for t in range(2):
        # At most one student per slot
        for s1 in range(8):
            for s2 in range(s1 + 1, 8):
                solver.add(Not(report[s1][d][t] & report[s2][d][t]))

# Tuesday is the only day George can give a report
for d in [0, 2]:  # Monday and Wednesday
    for t in range(2):
        solver.add(Not(report[GEORGE][d][t]))

# Olivia and Robert cannot give afternoon reports
for d in range(3):
    solver.add(Not(report[OLIVIA][d][1]))
    solver.add(Not(report[ROBERT][d][1]))

# Conditional Nina-Helen-Irving constraint
for d in range(2):  # Monday (0) and Tuesday (1); not Wednesday
    # If Nina reports on day d, then Helen and Irving must both report on day d+1
    nina_on_day_d = Or(report[NINA][d][0], report[NINA][d][1])
    # Helen and Irving must both report on day d+1 (exactly two reports that day)
    helen_on_day_d1 = Or(report[HELEN][d+1][0], report[HELEN][d+1][1])
    irving_on_day_d1 = Or(report[IRVING][d+1][0], report[IRVING][d+1][1])
    # Since exactly two reports per day, if both Helen and Irving report on d+1, they must be the only ones
    solver.add(Implies(nina_on_day_d, And(helen_on_day_d1, irving_on_day_d1)))

# Given assignments
solver.add(report[KYLE][1][1] == True)  # Kyle gives afternoon report on Tuesday
solver.add(report[HELEN][2][1] == True)  # Helen gives afternoon report on Wednesday

# Answer choices: [Mon_morning, Tue_morning, Wed_morning]
answer_choices = [
    (IRVING, LENORE, NINA),      # 0: Irving, Lenore, Nina
    (LENORE, GEORGE, IRVING),    # 1: Lenore, George, Irving
    (NINA, IRVING, LENORE),      # 2: Nina, Irving, Lenore
    (ROBERT, GEORGE, IRVING),    # 3: Robert, George, Irving
    (ROBERT, IRVING, LENORE)     # 4: Robert, Irving, Lenore
]

# Check each answer choice
answer_index_list = []
for idx, (mon_morning, tue_morning, wed_morning) in enumerate(answer_choices):
    s_chk = Solver()
    # Add all base constraints
    for a in solver.assertions():
        s_chk.add(a)
    
    # Add fixed assignments from the choice
    s_chk.add(report[mon_morning][0][0] == True)  # Monday morning
    s_chk.add(report[tue_morning][1][0] == True)  # Tuesday morning
    s_chk.add(report[wed_morning][2][0] == True)  # Wednesday morning
    
    # Ensure Tuesday has exactly two reports: Kyle (afternoon) + tue_morning (morning)
    # Already enforced by exactly-two-per-day constraint
    
    # Ensure Wednesday has exactly two reports: Helen (afternoon) + wed_morning (morning)
    # Already enforced by exactly-two-per-day constraint
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)