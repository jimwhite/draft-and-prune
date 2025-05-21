from z3 import *

# Define variables
assign_S = Array('assign_S', IntSort(), BoolSort())
assign_T = Array('assign_T', IntSort(), BoolSort())
assigned = Array('assigned', IntSort(), BoolSort())

solver = Solver()

# Define assigned[i]
for i in range(6):
    solver.add(assigned[i] == Or(assign_S[i], assign_T[i]))

# Constraint 1: At least two at each university
solver.add(Sum([If(assign_S[i], 1, 0) for i in range(6)]) >= 2)
solver.add(Sum([If(assign_T[i], 1, 0) for i in range(6)]) >= 2)

# Constraint 2: Exactly four assigned
solver.add(Sum([If(assigned[i], 1, 0) for i in range(6)]) == 4)

# Constraint 3: No photographer at both
# Corrected: Use Int('i') to create a Z3 integer constant
i = Int('i')
solver.add(ForAll([i], Implies(And(i >= 0, i < 6), Not(And(assign_S[i], assign_T[i])))))


# Constraint 4: Frost with Heideck
solver.add(assign_S[0] == assign_S[2])
solver.add(assign_T[0] == assign_T[2])

# Constraint 5: Lai and Mays different if both assigned
solver.add(Implies(And(assigned[4], assigned[5]), Xor(assign_S[4], assign_S[5])))

# Constraint 6: Gonzalez at Silva -> Lai at Thorne
solver.add(Implies(assign_S[1], assign_T[4]))

# Constraint 7: Knutson not at Thorne -> Heideck and Mays at Thorne
solver.add(Implies(Not(assign_T[3]), And(assign_T[2], assign_T[5])))

# Check answer choices
photographers = [0, 1, 3, 4, 5]  # Frost, Gonzalez, Knutson, Lai, Mays
for option_index, p_id in enumerate(photographers):
    solver.push()
    solver.add(Not(assign_S[p_id]))
    if solver.check() == unsat:
        print(f"Option {chr(65 + option_index)} is correct")
        exit()
    solver.pop()
