from z3 import *

singers = {'K': 0, 'L': 1, 'T': 2, 'W': 3, 'Y': 4, 'Z': 5}
singers_inv = {v: k for k, v in singers.items()}

def solve():
    solver = Solver()
    audition_order = [Int(f'slot_{i}') for i in range(6)]

    # All different constraint
    solver.add(Distinct(audition_order))
    for slot in audition_order:
        solver.add(And(slot >= 0, slot <= 5))

    # Base constraints
    solver.add(audition_order[singers['K']] < audition_order[singers['T']]) # Corrected index access
    solver.add(audition_order[singers['Z']] < audition_order[singers['Y']]) # Corrected index access

    recorded = [False] * 6
    recorded[singers['K']] = True # Access list by singer ID
    recorded[singers['L']] = True # Access list by singer ID
    recorded[3] = False
    recorded[4] = True
    
    for i in range(6):
        if recorded[i]:
            solver.add(Or(audition_order[i] == singers['K'], audition_order[i] == singers['L']))
        else:
            solver.add(And(audition_order[i] != singers['K'], audition_order[i] != singers['L']))


    # Original constraint
    original_constraint = If(audition_order[singers['K']] < audition_order[singers['L']], audition_order[singers['W']] < audition_order[singers['K']], audition_order[singers['W']] < audition_order[singers['L']]) # Use If to handle min correctly
    
    choices = [
        "Zinn's audition is the only one that can take place earlier than Waite's.",
        "Waite's audition must take place either immediately before or immediately after Zinn's.",
        "Waite's audition must take place earlier than Lugo's.",
        "Waite's audition must be either first or second.",
        "The first audition cannot be recorded."
    ]

    for i, choice in enumerate(choices):
        solver.push()
        solver.add(original_constraint)
        original_solutions = []
        while solver.check() == sat:
            model = solver.model()
            original_solutions.append(tuple(model[slot].as_long() for slot in audition_order))
            solver.add(Or([slot != model[slot] for slot in audition_order]))
        solver.pop()

        solver.push()
        if i == 0:  # Choice A
            alternative_constraint = And(audition_order[singers['W']] == audition_order[singers['Z']] + 1,
                                        And([audition_order[singers['W']] < audition_order[j] for j in range(6) if j != singers['Z']])) # Iterate over indices

        elif i == 1:  # Choice B
            alternative_constraint = Abs(audition_order[singers['W']] - audition_order[singers['Z']]) == 1

        elif i == 2:  # Choice C
            alternative_constraint = audition_order[singers['W']] < audition_order[singers['L']]

        elif i == 3:  # Choice D
            alternative_constraint = Or(audition_order[singers['W']] == 0, audition_order[singers['W']] == 1)

        elif i == 4:  # Choice E
            alternative_constraint = And(audition_order[0] != singers['K'], audition_order[0] != singers['L'])
        
        solver.add(alternative_constraint)
        alternative_solutions = []
        while solver.check() == sat:
            model = solver.model()
            alternative_solutions.append(tuple(model[slot].as_long() for slot in audition_order))
            solver.add(Or([slot != model[slot] for slot in audition_order]))
        solver.pop()

        if set(original_solutions) == set(alternative_solutions):
            print(f"Option {chr(65 + i)} is correct")
            return

solve()

