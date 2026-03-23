from z3 import *

# Define integer variables for Metro section counts: M_F, M_G, M_H
M_F = Int('M_F')
M_G = Int('M_G')
M_H = Int('M_H')

solver = Solver()

# Derived constraints from the premise (L_F=1, L_H=1, L_G=0) and other conditions:
# Metro total: M_F + M_G + M_H = 2
solver.add(M_F + M_G + M_H == 2)

# From step 9: M_F ∈ {0,1}, M_H ∈ {0,1}, M_G ∈ {1,2}
solver.add(M_F >= 0, M_F <= 1)
solver.add(M_H >= 0, M_H <= 1)
solver.add(M_G >= 1, M_G <= 2)

# Check each answer choice
answer_choices = [
    "Both Metro Fuentes",      # M_F == 2
    "Both Metro Gagnon",       # M_G == 2 and M_F == 0 and M_H == 0
    "Exactly one Metro Hue",   # M_H == 1
    "Both Sports Hue",         # S_H == 2 (but we know S_H = 1, so impossible)
    "Neither Sports Hue"       # S_H == 0 (but we know S_H = 1, so impossible)
]

# We already know from the premise and constraints that:
# S_F = 1, S_G = 0, S_H = 1 (so choices 3 and 4 are impossible)
# So we only need to check feasibility of choices 0, 1, 2

answer_index_list = []

# Choice 0: Both Metro Fuentes (M_F == 2)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(M_F == 2)
if s_chk.check() == unsat:
    # This choice is impossible, but we want to collect possible ones
    pass  # Not added to answer_index_list

# Choice 1: Both Metro Gagnon (M_G == 2, M_F == 0, M_H == 0)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(M_G == 2, M_F == 0, M_H == 0)
if s_chk.check() == sat:
    answer_index_list.append(1)

# Choice 2: Exactly one Metro Hue (M_H == 1)
s_chk = Solver()
s_chk.add(solver.assertions())
s_chk.add(M_H == 1)
if s_chk.check() == sat:
    answer_index_list.append(2)

# Choice 3: Both Sports Hue (S_H == 2) - impossible due to fixed S_H = 1
# We know from premise: L_F=1, L_H=1 => S_F = L_H = 1; Sports total = 2, S_G=0 => S_H must be 1
# So this is impossible by construction; no need to check

# Choice 4: Neither Sports Hue (S_H == 0) - also impossible for same reason

# However, per the plan, we should verify choices 3 and 4 using Z3 with full model
# Let's do a more complete check including all variables to be safe

# Full model for verification
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F_full, M_G_full, M_H_full = Ints('M_F M_G M_H')
S_F_full, S_G_full, S_H_full = Ints('S_F S_G S_H')

solver_full = Solver()

# Section size constraints
solver_full.add(L_F + L_G + L_H == 2)
solver_full.add(M_F_full + M_G_full + M_H_full == 2)
solver_full.add(S_F_full + S_G_full + S_H_full == 2)

# Global photographer count constraints
F_total = L_F + M_F_full + S_F_full
G_total = L_G + M_G_full + S_G_full
H_total = L_H + M_H_full + S_H_full

solver_full.add(F_total >= 1, F_total <= 3)
solver_full.add(G_total >= 1, G_total <= 3)
solver_full.add(H_total >= 1, H_total <= 3)

# At-least-one-Metro-co photographer-in-Lifestyle constraint
# (L_F > 0 ∧ M_F_full > 0) ∨ (L_G > 0 ∧ M_G_full > 0) ∨ (L_H > 0 ∧ M_H_full > 0)
b1 = And(L_F > 0, M_F_full > 0)
b2 = And(L_G > 0, M_G_full > 0)
b3 = And(L_H > 0, M_H_full > 0)
solver_full.add(Or(b1, b2, b3))

# Lifestyle-Fuentes-Sports-Hue equality constraint
solver_full.add(L_H == S_F_full)

# Gagnon-no-Sports constraint
solver_full.add(S_G_full == 0)

# Premise: L_F = 1, L_H = 1
solver_full.add(L_F == 1)
solver_full.add(L_H == 1)

# Now check each answer choice with full model
answer_index_list_full = []

# Choice 0: Both Metro Fuentes (M_F_full == 2)
s_chk = Solver()
s_chk.add(solver_full.assertions())
s_chk.add(M_F_full == 2)
if s_chk.check() == unsat:
    pass
else:
    answer_index_list_full.append(0)

# Choice 1: Both Metro Gagnon (M_G_full == 2, M_F_full == 0, M_H_full == 0)
s_chk = Solver()
s_chk.add(solver_full.assertions())
s_chk.add(M_G_full == 2, M_F_full == 0, M_H_full == 0)
if s_chk.check() == sat:
    answer_index_list_full.append(1)

# Choice 2: Exactly one Metro Hue (M_H_full == 1)
s_chk = Solver()
s_chk.add(solver_full.assertions())
s_chk.add(M_H_full == 1)
if s_chk.check() == sat:
    answer_index_list_full.append(2)

# Choice 3: Both Sports Hue (S_H_full == 2)
s_chk = Solver()
s_chk.add(solver_full.assertions())
s_chk.add(S_H_full == 2)
if s_chk.check() == unsat:
    pass
else:
    answer_index_list_full.append(3)

# Choice 4: Neither Sports Hue (S_H_full == 0)
s_chk = Solver()
s_chk.add(solver_full.assertions())
s_chk.add(S_H_full == 0)
if s_chk.check() == unsat:
    pass
else:
    answer_index_list_full.append(4)

# Print the list of possible choices (indices)
print(answer_index_list_full)