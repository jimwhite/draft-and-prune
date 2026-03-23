from z3 import *

# Student indices
(G, H, I, K, L, N, O, R) = range(8)

# Boolean variables: whether each student gives a report
report = [Bool(f"report_{i}") for i in range(8)]

# Base solver
solver = Solver()

# Exactly six students give reports
solver.add(Sum([If(report[i], 1, 0) for i in range(8)]) == 6)

# Slot variables: each slot is assigned a student index (or -1 if not used, but we'll enforce exactly 6 slots)
# Monday: morning (M_m), afternoon (M_a); Tuesday: T_m, T_a; Wednesday: W_m, W_a
slots = [
    [Int(f"M_m"), Int(f"M_a")],  # Monday
    [Int(f"T_m"), Int(f"T_a")],  # Tuesday
    [Int(f"W_m"), Int(f"W_a")]   # Wednesday
]

# Assignment constraints: each slot must be filled by a student who reports, and all reportees are distinct
all_slots = [slots[0][0], slots[0][1], slots[1][0], slots[1][1], slots[2][0], slots[2][1]]
solver.add(Distinct(*all_slots))

# Each slot must be assigned to a student who reports
for i in range(3):
    for j in range(2):
        slot_var = slots[i][j]
        # slot_var must be one of the students who reports
        disj = []
        for s in range(8):
            disj.append(And(slot_var == s, report[s]))
        solver.add(Or(*disj))

# Availability constraints
# Tuesday is the only day George can report: if George reports, he must be in a Tuesday slot
solver.add(Implies(report[G], Or(slots[1][0] == G, slots[1][1] == G)))

# Neither Olivia nor Robert can give an afternoon report
solver.add(Implies(report[O], Or(slots[0][0] == O, slots[1][0] == O, slots[2][0] == O)))
solver.add(Implies(report[R], Or(slots[0][0] == R, slots[1][0] == R, slots[2][0] == R)))

# Nina conditional constraint
# If Nina reports and is not on Wednesday, then Helen and Irving must both report the next day
# We'll encode this using implications for each possible Nina slot

# Helper: function to check if a student is in a specific day's slots
def on_day(student, day):
    return Or(slots[day][0] == student, slots[day][1] == student)

# Nina on Monday → Helen and Irving must both report on Tuesday
nina_mon_impl = Implies(And(report[N], on_day(N, 0)), And(report[H], report[I], on_day(H, 1), on_day(I, 1)))

# Nina on Tuesday → Helen and Irving must both report on Wednesday
nina_tue_impl = Implies(And(report[N], on_day(N, 1)), And(report[H], report[I], on_day(H, 2), on_day(I, 2)))

# Nina on Wednesday → no constraint
solver.add(Or(
    Not(report[N]),
    And(report[N], on_day(N, 2)),  # Nina on Wednesday
    nina_mon_impl,
    nina_tue_impl
))

# Given condition: Kyle and Lenore do NOT give reports
solver.add(Not(report[K]), Not(report[L]))

# Answer choices: morning reports on Monday, Tuesday, Wednesday respectively
answer_choices = [
    (H, G, N),  # 'Helen, George, and Nina'
    (I, R, H),  # 'Irving, Robert, and Helen'
    (N, H, O),  # 'Nina, Helen, and Olivia'
    (O, R, I),  # 'Olivia, Robert, and Irving'
    (R, G, H)   # 'Robert, George, and Helen'
]

# Check each answer choice
answer_index_list = []
for idx, (mon_morn, tue_morn, wed_morn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert morning slots for each day
    s_chk.add(slots[0][0] == mon_morn)
    s_chk.add(slots[1][0] == tue_morn)
    s_chk.add(slots[2][0] == wed_morn)
    
    # Ensure the students assigned to morning slots actually report
    s_chk.add(report[mon_morn])
    s_chk.add(report[tue_morn])
    s_chk.add(report[wed_morn])
    
    # Check if this configuration is possible
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)