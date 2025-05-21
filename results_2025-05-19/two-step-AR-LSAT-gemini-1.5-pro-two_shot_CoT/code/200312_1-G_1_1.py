from z3 import *

def solve_scientist_selection():
    F, G, H, K, L, M, P, Q, R = Bools('F G H K L M P Q R')
    scientists = [F, G, H, K, L, M, P, Q, R]
    options = [
        [F, G, K, P, Q],
        [G, H, K, L, M],
        [G, H, K, L, R],
        [H, K, M, P, R],
        [H, L, M, P, Q]
    ]

    for i, option in enumerate(options):
        solver = Solver()

        # Constraint 2
        solver.add(Or(F, G, H))
        solver.add(Or(K, L, M))
        solver.add(Or(P, Q, R))

        # Constraint 3
        solver.add(Implies(And(Or(F,G), Or(F,H), Or(G,H)), Not(And(P,Q))))
        solver.add(Implies(And(Or(F,G), Or(F,H), Or(G,H)), Not(And(P,R))))
        solver.add(Implies(And(Or(F,G), Or(F,H), Or(G,H)), Not(And(Q,R))))


        # Constraint 4
        solver.add(Not(And(F, K)))

        # Constraint 5
        solver.add(Not(And(K, M)))

        # Constraint 6
        solver.add(Implies(M, And(P, R)))

        # Constraints for the current option
        selected_scientists = []
        for j, s in enumerate(scientists):
            if s in option:
                solver.add(s == True)
                selected_scientists.append(s)
            else:
                solver.add(s == False)

        # Constraint 1 (Panel Size)
        solver.add(Sum([If(s, 1, 0) for s in scientists]) == 5)


        if solver.check() == sat:
            print(f"Option {chr(65 + i)} is correct")
            return

solve_scientist_selection()