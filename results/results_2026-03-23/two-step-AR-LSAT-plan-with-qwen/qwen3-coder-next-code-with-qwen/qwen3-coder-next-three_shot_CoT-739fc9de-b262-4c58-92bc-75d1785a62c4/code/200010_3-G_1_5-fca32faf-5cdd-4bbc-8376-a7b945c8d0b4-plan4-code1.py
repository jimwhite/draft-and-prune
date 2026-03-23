from z3 import *

# Student indices: George, Helen, Irving, Kyle, Lenore, Nina, Olivia, Robert
(G, H, I, K, L, N, O, R) = range(8)
students = ["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"]

# Define slots: morning and afternoon for each day
# Monday: 0-morning, 1-afternoon; Tuesday: 2-morning, 3-afternoon; Wednesday: 4-morning, 5-afternoon
slots = ["M_m", "M_a", "T_m", "T_a", "W_m", "W_a"]

# Create Boolean variables: assigned[s][slot_idx] = True if student s is assigned to slot
assigned = [[Bool(f"assigned_{s}_{slot}") for slot in range(6)] for s in range(8)]

# Base solver
solver = Solver()

# Exactly six reporters constraint
solver.add(Sum([If(assigned[s][slot], 1, 0) for s in range(8) for slot in range(6)]) == 6)

# Two reports per day constraint
for day in range(3):
    morning_slot = 2 * day
    afternoon_slot = 2 * day + 1
    # Exactly one student per slot, and exactly two slots per day are assigned
    for slot in [morning_slot, afternoon_slot]:
        solver.add(Sum([If(assigned[s][slot], 1, 0) for s in range(8)]) == 1)

# Slot uniqueness per student: each student gives at most one report
for s in range(8):
    solver.add(Sum([If(assigned[s][slot], 1, 0) for slot in range(6)]) <= 1)

# Tuesday-only-for-George constraint: George can only give reports on Tuesday
for slot in [0, 1, 4, 5]:  # Monday morning, Monday afternoon, Wednesday morning, Wednesday afternoon
    solver.add(Not(assigned[G][slot]))

# No-afternoon-for-Olivia-and-Robert constraint
for slot in [1, 3, 5]:  # afternoon slots: Monday, Tuesday, Wednesday
    solver.add(Not(assigned[O][slot]), Not(assigned[R][slot]))

# Nina conditional constraint
# If Nina gives a report on Monday (slot 0 or 1), then Helen and Irving must both give reports on Tuesday
# If Nina gives a report on Tuesday (slot 2 or 3), then Helen and Irving must both give reports on Wednesday
# If Nina gives a report on Wednesday (slot 4 or 5), no condition applies

# Nina Monday -> Helen and Irving Tuesday
nina_monday = Or(assigned[N][0], assigned[N][1])
helen_tue = Or(assigned[H][2], assigned[H][3])
irving_tue = Or(assigned[I][2], assigned[I][3])
solver.add(Implies(nina_monday, And(helen_tue, irving_tue)))

# Nina Tuesday -> Helen and Irving Wednesday
nina_tue = Or(assigned[N][2], assigned[N][3])
helen_wed = Or(assigned[H][4], assigned[H][5])
irving_wed = Or(assigned[I][4], assigned[I][5])
solver.add(Implies(nina_tue, And(helen_wed, irving_wed)))

# Given assignments: Kyle gives afternoon report on Tuesday (slot 3), Helen gives afternoon report on Wednesday (slot 5)
solver.add(assigned[K][3])
solver.add(assigned[H][5])

# Now check each answer choice
answer_choices = [
    ("Irving", "Lenore", "Nina"),   # Monday, Tuesday, Wednesday morning reports
    ("Lenore", "George", "Irving"),
    ("Nina", "Irving", "Lenore"),
    ("Robert", "George", "Irving"),
    ("Robert", "Irving", "Lenore")
]

# Map student names to indices
student_map = {name: idx for idx, name in enumerate(students)}

answer_index_list = []
for idx, (mon_morn, tue_morn, wed_morn) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints for morning reports
    mon_morn_idx = student_map[mon_morn]
    tue_morn_idx = student_map[tue_morn]
    wed_morn_idx = student_map[wed_morn]
    
    # Assign morning slots
    s_chk.add(assigned[mon_morn_idx][0])  # Monday morning (slot 0)
    s_chk.add(assigned[tue_morn_idx][2])  # Tuesday morning (slot 2)
    s_chk.add(assigned[wed_morn_idx][4])  # Wednesday morning (slot 4)
    
    # Additional consistency checks:
    # - Kyle is already assigned to Tuesday afternoon (slot 3), so he can't be Tuesday morning
    # - George can only be on Tuesday, and we already have Kyle on Tuesday afternoon, so if George is Tuesday morning, that's fine
    # - Olivia and Robert can't be in afternoon slots (already handled by base constraints)
    
    # Ensure no student appears twice
    # Already enforced by "slot uniqueness per student" constraint
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)