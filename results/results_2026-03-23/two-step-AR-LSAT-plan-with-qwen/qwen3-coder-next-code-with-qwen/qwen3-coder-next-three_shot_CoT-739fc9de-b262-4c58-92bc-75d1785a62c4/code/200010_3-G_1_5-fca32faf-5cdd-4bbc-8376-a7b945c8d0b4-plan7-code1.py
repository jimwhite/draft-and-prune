from z3 import *

# Student indices
(G, H, I, K, L, N, O, R) = range(8)

# r[i][d][s] = True if student i gives report on day d (0=Mon,1=Tue,2=Wed) in slot s (0=morning,1=afternoon)
r = [[[Bool(f"r_{i}_{d}_{s}") for s in range(2)] for d in range(3)] for i in range(8)]

solver = Solver()

# Exactly six reports total
solver.add(Sum([If(r[i][d][s], 1, 0) for i in range(8) for d in range(3) for s in range(2)]) == 6)

# Two reports per day (one morning, one afternoon)
for d in range(3):
    solver.add(Sum([r[i][d][s] for i in range(8) for s in range(2)]) == 2)

# One report per slot (exactly one student per slot)
for d in range(3):
    for s in range(2):
        solver.add(Sum([r[i][d][s] for i in range(8)]) == 1)

# George can only report on Tuesday
for d in [0, 2]:  # Monday and Wednesday
    for s in range(2):
        solver.add(Not(r[G][d][s]))

# Olivia and Robert cannot give afternoon reports
for student in [O, R]:
    for d in range(3):
        solver.add(Not(r[student][d][1]))

# Nina implication constraint
for d in range(2):  # Monday (0) and Tuesday (1)
    # If Nina reports on day d, then Helen and Irving must both report on day d+1
    # Since exactly one per slot, this means Helen and Irving take both slots on d+1
    nina_on_day_d = Or(r[N][d][0], r[N][d][1])
    helen_on_next = Or(r[H][d+1][0], r[H][d+1][1])
    irving_on_next = Or(r[I][d+1][0], r[I][d+1][1])
    solver.add(Implies(nina_on_day_d, And(helen_on_next, irving_on_next)))

# Given conditions
solver.add(r[K][1][1] == True)  # Kyle gives afternoon report on Tuesday
solver.add(r[H][2][1] == True)  # Helen gives afternoon report on Wednesday

# Answer choices: each is [Mon_morning, Tue_morning, Wed_morning]
answer_choices = [
    (I, L, N),  # Irving, Lenore, Nina
    (L, G, I),  # Lenore, George, Irving
    (N, I, L),  # Nina, Irving, Lenore
    (R, G, I),  # Robert, George, Irving
    (R, I, L)   # Robert, Irving, Lenore
]

# Check each answer choice
answer_index_list = []
for idx, (mon_morn, tue_morn, wed_morn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for the specified morning reports
    s_chk.add(r[mon_morn][0][0] == True)
    s_chk.add(r[tue_morn][1][0] == True)
    s_chk.add(r[wed_morn][2][0] == True)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)