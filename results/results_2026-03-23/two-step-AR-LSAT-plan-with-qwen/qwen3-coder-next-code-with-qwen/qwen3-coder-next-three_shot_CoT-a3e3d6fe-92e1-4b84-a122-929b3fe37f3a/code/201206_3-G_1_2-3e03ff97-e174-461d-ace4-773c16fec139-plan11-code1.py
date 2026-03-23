from z3 import *

# Lab assistant indices: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
(J, K, L, N, O, R) = range(6)

# Session indices: 0-5 (0=Wed morning, 1=Wed afternoon, 2=Thu morning, 3=Thu afternoon, 4=Fri morning, 5=Fri afternoon)
assign = [Int(f"assign_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each assistant assigned to exactly one session (0-5)
for i in range(6):
    solver.add(assign[i] >= 0, assign[i] <= 5)

# All assignments distinct
solver.add(Distinct(*assign))

# Kevin and Rebecca must lead sessions on the same day
solver.add((assign[K] - assign[R]) % 2 == 0)

# Lan and Olivia cannot lead sessions on the same day
solver.add((assign[L] - assign[O]) % 2 != 0)

# Nessa must lead an afternoon session
solver.add(assign[N] % 2 == 1)

# Julio's session must be on an earlier day than Olivia's
solver.add(assign[J] < assign[O])
solver.add(IntVal(assign[J] // 2) < IntVal(assign[O] // 2))

# Premise: Lan does not lead a Wednesday session
solver.add(assign[L] >= 2)

# Answer choices indices: ['Rebecca', 'Olivia', 'Nessa', 'Kevin', 'Julio']
answer_choices = [R, O, N, K, J]

# Check each answer choice
answer_index_list = []
for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint that this assistant does NOT lead any Thursday session
    s_chk.add(assign[assistant] < 2)
    
    # If UNSAT, this assistant must lead a Thursday session
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)