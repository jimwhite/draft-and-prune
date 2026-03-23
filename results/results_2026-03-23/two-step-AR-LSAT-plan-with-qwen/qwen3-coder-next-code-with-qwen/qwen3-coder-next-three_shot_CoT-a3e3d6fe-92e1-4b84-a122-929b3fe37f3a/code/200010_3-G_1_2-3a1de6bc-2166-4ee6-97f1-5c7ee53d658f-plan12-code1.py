from z3 import *

# Student indices
(STUDENTS, idx_map) = (["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"], {})
for i, s in enumerate(STUDENTS):
    idx_map[s] = i

# Days: 0=Monday, 1=Tuesday, 2=Wednesday
# Times: 0=morning, 1=afternoon
assigned = [[[Bool(f"assigned_{s}_{d}_{t}") for t in range(2)] for d in range(3)] for s in range(8)]

solver = Solver()

# Exactly six reporters
total_reports = Sum([If(assigned[s][d][t], 1, 0) 
                     for s in range(8) for d in range(3) for t in range(2)])
solver.add(total_reports == 6)

# Two reports per day
for d in range(3):
    solver.add(Sum([assigned[s][d][t] for s in range(8) for t in range(2)]) == 2)

# One report per student (at most one slot)
for s in range(8):
    solver.add(Sum([assigned[s][d][t] for d in range(3) for t in range(2)]) <= 1)

# George only on Tuesday
for d in [0, 2]:  # Monday and Wednesday
    for t in range(2):
        solver.add(Not(assigned[idx_map["George"]][d][t]))

# Olivia and Robert cannot give afternoon reports
for s_name in ["Olivia", "Robert"]:
    for d in range(3):
        solver.add(Not(assigned[idx_map[s_name]][d][1]))

# Nina implication constraint
# If Nina gives a report on Monday, then Helen and Irving must both give reports on Tuesday
nina_mon = assigned[idx_map["Nina"]][0][0]
helen_tue = Or(assigned[idx_map["Helen"]][1][0], assigned[idx_map["Helen"]][1][1])
irving_tue = Or(assigned[idx_map["Irving"]][1][0], assigned[idx_map["Irving"]][1][1])
solver.add(Implies(nina_mon, And(helen_tue, irving_tue)))

# If Nina gives a report on Tuesday, then Helen and Irving must both give reports on Wednesday
nina_tue = Or(assigned[idx_map["Nina"]][1][0], assigned[idx_map["Nina"]][1][1])
helen_wed = Or(assigned[idx_map["Helen"]][2][0], assigned[idx_map["Helen"]][2][1])
irving_wed = Or(assigned[idx_map["Irving"]][2][0], assigned[idx_map["Irving"]][2][1])
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))

# Kyle and Lenore do not give reports
for s_name in ["Kyle", "Lenore"]:
    for d in range(3):
        for t in range(2):
            solver.add(Not(assigned[idx_map[s_name]][d][t]))

# Answer choices: each is a list of 3 students for Monday morning, Tuesday morning, Wednesday morning
answer_choices = [
    ["Helen", "George", "Nina"],
    ["Irving", "Robert", "Helen"],
    ["Nina", "Helen", "Olivia"],
    ["Olivia", "Robert", "Irving"],
    ["Robert", "George", "Helen"]
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for the morning reports
    # Monday morning = choice[0]
    s_chk.add(assigned[idx_map[choice[0]]][0][0])
    
    # Tuesday morning = choice[1]
    s_chk.add(assigned[idx_map[choice[1]]][1][0])
    
    # Wednesday morning = choice[2]
    s_chk.add(assigned[idx_map[choice[2]]][2][0])
    
    # Additional constraints to ensure consistency:
    # - George only on Tuesday: if choice[1] is not "George", then we already have constraint that George can't be on Mon/Wed, but need to ensure he's not assigned elsewhere
    # - Olivia/Robert only in morning: already handled by afternoon constraints
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)