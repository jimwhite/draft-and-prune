from z3 import *

# Variables
article_at_slot = Array('article_at_slot', IntSort(), IntSort())
i = Int('i')

# Solver
solver = Solver()

# Constraints
solver.add(ForAll([i], Implies(And(i >= 1, i <= 7), And(article_at_slot[i] >= 0, article_at_slot[i] <= 6)))) # Constraint 0
solver.add(Distinct([article_at_slot[i] for i in range(1, 8)])) # Constraint 1
solver.add(ForAll([i], Implies(And(i >= 1, i <= 6),
        Or(
            And(article_at_slot[i] < 3, article_at_slot[i+1] < 3),
            And(article_at_slot[i] > 2, article_at_slot[i] < 6, article_at_slot[i+1] > 2, article_at_slot[i+1] < 6),
            And(article_at_slot[i] == 6, article_at_slot[i+1] == 6),
            And(article_at_slot[i+1] == 6, article_at_slot[i] == 6)
        )))) # Constraint 2
solver.add(Implies(article_at_slot[5] < article_at_slot[3], article_at_slot[3] == 3)) # Constraint 3
solver.add(article_at_slot[5] < article_at_slot[6]) # Constraint 4
# Corrected Constraint 5: Chained comparisons are not supported, use And instead
solver.add(And(article_at_slot[2] < article_at_slot[1], article_at_slot[1] < article_at_slot[4])) # Constraint 5


# Answer choices
answer_choices = [
    (4, 1),  # H is fourth
    (6, 1),  # H is sixth
    (4, 4),  # R is fourth
    (7, 4),  # R is seventh
    (5, 6)   # Y is fifth
]

for choice_index, (slot, article_id) in enumerate(answer_choices):
    solver.push()
    solver.add(article_at_slot[slot] == article_id)
    if solver.check() == sat:
        model = solver.model()
        is_unique = True
        for slot_idx in range(1, 8):
            original_value = model[article_at_slot[slot_idx]].as_long()
            solver.push()
            solver.add(article_at_slot[slot_idx] != original_value)
            if solver.check() == sat:
                is_unique = False
                solver.pop()
                break
            solver.pop()
        if is_unique:
            print(f"Option {chr(65 + choice_index)} is correct")
            exit()
    solver.pop()
