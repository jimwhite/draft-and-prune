from z3 import *

# Student indices
(STUDENTS, idx_map) = (["George", "Helen", "Irving", "Kyle", "Lenore", "Nina", "Olivia", "Robert"], {})
for i, s in enumerate(STUDENTS):
    idx_map[s] = i

# Slot variables: M_M, M_A, T_M, T_A, W_M, W_A (each is an integer index of student)
M_M = Int("M_M")
M_A = Int("M_A")
T_M = Int("T_M")
T_A = Int("T_A")
W_M = Int("W_M")
W_A = Int("W_A")

solver = Solver()

# Domain constraints: each slot must be one of the 8 students
for var in [M_M, M_A, T_M, T_A, W_M, W_A]:
    solver.add(Or([var == idx_map[s] for s in STUDENTS]))

# Injectivity: exactly 6 distinct students assigned to the 6 slots
solver.add(Distinct(M_M, M_A, T_M, T_A, W_M, W_A))

# Fixed constraints from scenario
solver.add(T_A == idx_map["Kyle"])  # Kyle gives afternoon report on Tuesday
solver.add(W_A == idx_map["Helen"]) # Helen gives afternoon report on Wednesday

# Tuesday is the only day George can give a report
solver.add(T_M == idx_map["George"])  # Since T_A is Kyle, George must be Tuesday morning
solver.add(M_M != idx_map["George"])
solver.add(M_A != idx_map["George"])
solver.add(W_M != idx_map["George"])

# Afternoon report constraints: Olivia and Robert cannot give afternoon reports
solver.add(M_A != idx_map["Olivia"])
solver.add(M_A != idx_map["Robert"])
# T_A and W_A already fixed to Kyle and Helen, so no need to add more constraints

# Nina conditional constraint: Nina can only be in W_M (Wednesday morning)
# If Nina is in any other slot, it's invalid
solver.add(M_M != idx_map["Nina"])
solver.add(M_A != idx_map["Nina"])
solver.add(T_M != idx_map["Nina"])  # Already enforced by T_M = George
solver.add(T_A != idx_map["Nina"])  # Already enforced by T_A = Kyle

# Answer choices: each is a tuple (M_M, T_M, W_M)
answer_choices = [
    ("Irving", "Lenore", "Nina"),      # Choice 0
    ("Lenore", "George", "Irving"),   # Choice 1
    ("Nina", "Irving", "Lenore"),     # Choice 2
    ("Robert", "George", "Irving"),   # Choice 3
    ("Robert", "Irving", "Lenore")    # Choice 4
]

# Check each answer choice
answer_index_list = []
for idx, (mm_str, tm_str, wm_str) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraints from the answer choice
    # T_M must be George (already in global constraints), so tm_str must be "George"
    if tm_str != "George":
        # Skip invalid choices where Tuesday morning is not George
        continue
    
    s_chk.add(M_M == idx_map[mm_str])
    s_chk.add(T_M == idx_map["George"])  # Redundant but explicit
    s_chk.add(W_M == idx_map[wm_str])
    
    # Check if all 6 assigned students are distinct
    # Already handled by Distinct constraint, but ensure no conflict with fixed assignments
    if mm_str in ["Kyle", "Helen"] or wm_str in ["Kyle", "Helen"]:
        # Kyle and Helen are already assigned to T_A and W_A respectively
        continue
    
    if mm_str == "George" or wm_str == "George":
        # George is only on Tuesday morning
        continue
    
    if mm_str == wm_str:
        # M_M and W_M must be distinct
        continue
    
    if mm_str in ["Irving", "Lenore", "Nina", "Olivia", "Robert"]:
        # Check Nina constraint: if wm_str == "Nina", it's okay (only valid slot for Nina)
        # If mm_str == "Nina" or wm_str == "Nina", already handled by above constraints
        pass
    
    # Check afternoon slot M_A: must be filled with a student not yet used
    # Students already assigned: mm_str, George, Kyle, wm_str, Helen
    used = {mm_str, "George", "Kyle", wm_str, "Helen"}
    
    # M_A must be one of the remaining students
    available = [s for s in STUDENTS if s not in used and s != mm_str and s != "George" and s != "Kyle" and s != wm_str and s != "Helen"]
    
    # Add constraint that M_A is one of the available students
    s_chk.add(Or([M_A == idx_map[s] for s in available]))
    
    # Check if Nina is used and not in W_M (invalid)
    if mm_str == "Nina" or wm_str != "Nina" and "Nina" in used:
        # Nina must be either not assigned or only in W_M
        if mm_str == "Nina" or (wm_str != "Nina" and "Nina" in used):
            continue
    
    # Check afternoon constraints: M_A cannot be Olivia or Robert
    s_chk.add(M_A != idx_map["Olivia"])
    s_chk.add(M_A != idx_map["Robert"])
    
    # Check if model is satisfiable
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)