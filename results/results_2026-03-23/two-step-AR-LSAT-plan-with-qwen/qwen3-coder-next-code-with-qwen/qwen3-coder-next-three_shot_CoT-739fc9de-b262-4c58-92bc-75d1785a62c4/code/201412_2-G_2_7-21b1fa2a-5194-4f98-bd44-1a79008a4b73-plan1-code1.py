from z3 import *

# Art historians: 0-Farley, 1-Garcia, 2-Holden, 3-Jiang
# Topics: 0-lithographs, 1-oil paintings, 2-sculptures, 3-watercolors

# Position variables: pos[i] = lecture position (1-4) for historian i
pos = [Int(f"pos_{i}") for i in range(4)]

# Topic assignment variables: topic[i] = topic given by historian i
topic = [Int(f"topic_{i}") for i in range(4)]

solver = Solver()

# Domain constraints: positions 1-4, all distinct
for i in range(4):
    solver.add(pos[i] >= 1, pos[i] <= 4)
solver.add(Distinct(*pos))

# Topic constraints: each topic assigned exactly once
for i in range(4):
    solver.add(topic[i] >= 0, topic[i] <= 3)
solver.add(Distinct(*topic))

# Use boolean indicators to find which historian gives each topic
litho_hist = [Bool(f"litho_hist_{i}") for i in range(4)]
oil_hist = [Bool(f"oil_hist_{i}") for i in range(4)]
water_hist = [Bool(f"water_hist_{i}") for i in range(4)]

# Exactly one historian gives lithographs
solver.add(PbEq([(litho_hist[i], 1) for i in range(4)], 1))
# Exactly one historian gives oil paintings
solver.add(PbEq([(oil_hist[i], 1) for i in range(4)], 1))
# Exactly one historian gives watercolors
solver.add(PbEq([(water_hist[i], 1) for i in range(4)], 1))

# Link topic assignments with historian indicators
for i in range(4):
    solver.add(Implies(litho_hist[i], topic[i] == 0))
    solver.add(Implies(oil_hist[i], topic[i] == 1))
    solver.add(Implies(water_hist[i], topic[i] == 3))

# Oil paintings and watercolors lectures earlier than lithographs
solver.add(Sum([If(litho_hist[i], pos[i], 0) for i in range(4)]) > 
           Sum([If(oil_hist[i], pos[i], 0) for i in range(4)]))
solver.add(Sum([If(litho_hist[i], pos[i], 0) for i in range(4)]) > 
           Sum([If(water_hist[i], pos[i], 0) for i in range(4)]))

# Farley's lecture earlier than oil paintings lecture
farley = 0
solver.add(pos[farley] < Sum([If(oil_hist[i], pos[i], 0) for i in range(4)]))

# Holden's lecture earlier than Garcia's and Jiang's
holden = 2
garcia = 1
jiang = 3
solver.add(pos[holden] < pos[garcia])
solver.add(pos[holden] < pos[jiang])

# Answer choices as conditions
# A: Farley's lecture earlier than sculptures lecture (topic == 2)
sculpt_hist = [Bool(f"sculpt_hist_{i}") for i in range(4)]
solver.add(PbEq([(sculpt_hist[i], 1) for i in range(4)], 1))
for i in range(4):
    solver.add(Implies(sculpt_hist[i], topic[i] == 2))

cond_A = pos[farley] < Sum([If(sculpt_hist[i], pos[i], 0) for i in range(4)])

# B: Holden's lecture earlier than lithographs lecture
cond_B = pos[holden] < Sum([If(litho_hist[i], pos[i], 0) for i in range(4)])

# C: Sculptures lecture earlier than Garcia's lecture
cond_C = Sum([If(sculpt_hist[i], pos[i], 0) for i in range(4)]) < pos[garcia]

# D: Sculptures lecture earlier than Jiang's lecture
cond_D = Sum([If(sculpt_hist[i], pos[i], 0) for i in range(4)]) < pos[jiang]

# E: Watercolors lecture earlier than Garcia's lecture
cond_E = Sum([If(water_hist[i], pos[i], 0) for i in range(4)]) < pos[garcia]

# Check which conditions hold in all models
answer_index_list = []
for idx, cond in enumerate([cond_A, cond_B, cond_C, cond_D, cond_E]):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add negation of condition
    s_chk.add(Not(cond))
    
    if s_chk.check() == unsat:
        # Condition must be true in all models
        answer_index_list.append(idx)

print(answer_index_list)