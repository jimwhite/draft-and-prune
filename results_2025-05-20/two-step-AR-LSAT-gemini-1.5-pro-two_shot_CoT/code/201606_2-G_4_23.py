from z3 import *

# Entities (Singer IDs)
K, L, T, W, Y, Z = 0, 1, 2, 3, 4, 5

# Variables
audition_order = Array('audition_order', IntSort(), IntSort())
recorded = Array('recorded', IntSort(), BoolSort())
k_slot, l_slot, t_slot, w_slot, y_slot, z_slot = Ints('k_slot l_slot t_slot w_slot y_slot z_slot')
i = Int('i')
s_slot = Int('s_slot')


# Constraints
def define_constraints(solver):
    # C0 (Domain of audition_order)
    solver.add(ForAll([i], Implies(And(i >= 1, i <= 6), And(audition_order[i] >= 0, audition_order[i] <= 5))))

    # C_Slots (Domain and Distinctness of singer slots)
    solver.add(Distinct(k_slot, l_slot, t_slot, w_slot, y_slot, z_slot))
    solver.add(And([And(s >= 1, s <= 6) for s in [k_slot, l_slot, t_slot, w_slot, y_slot, z_slot]]))

    # C_Mapping (Map slots to singers)
    solver.add(audition_order[k_slot] == K)
    solver.add(audition_order[l_slot] == L)
    solver.add(audition_order[t_slot] == T)
    solver.add(audition_order[w_slot] == W)
    solver.add(audition_order[y_slot] == Y)
    solver.add(audition_order[z_slot] == Z)

    # C2 (Kammer and Lugo recorded)
    solver.add(recorded[k_slot] == True)
    solver.add(recorded[l_slot] == True)

    # C3 (Others not recorded)
    solver.add(recorded[t_slot] == False)
    solver.add(recorded[w_slot] == False)
    solver.add(recorded[y_slot] == False)
    solver.add(recorded[z_slot] == False)

    # C4 (Fourth not recorded)
    solver.add(recorded[4] == False)

    # C5 (Fifth recorded)
    solver.add(recorded[5] == True)

    # C7 (Kammer before Trillo)
    solver.add(k_slot < t_slot)

    # C8 (Zinn before Yoshida)
    solver.add(z_slot < y_slot)


# Original Constraint
C6_Original = And(w_slot < k_slot, w_slot < l_slot)

# Answer Choices and their corresponding constraints
answer_choices = [
    ForAll([s_slot], Implies(And(s_slot >= 1, s_slot <= 6, s_slot < w_slot), audition_order[s_slot] == Z)),
    Or(w_slot == z_slot - 1, w_slot == z_slot + 1),
    w_slot < l_slot,
    Or(w_slot == 1, w_slot == 2),
    recorded[1] == False
]

# Check each answer choice
for i, alt_constraint in enumerate(answer_choices):
    solver = Solver()
    define_constraints(solver)

    # Check 1 (O implies Alt)
    solver.push()
    solver.add(C6_Original)
    solver.add(Not(alt_constraint))
    check1 = solver.check()
    solver.pop()

    # Check 2 (Alt implies O)
    solver.push()
    solver.add(alt_constraint)
    solver.add(Not(C6_Original))
    check2 = solver.check()
    solver.pop()

    if check1 == unsat and check2 == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()

