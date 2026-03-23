from z3 import *

# Cookie types: 0=oatmeal, 1=peanut butter, 2=sugar
# Batch numbers: 0=first, 1=second, 2=third
day = [[Int(f"day_{t}_{b}") for b in range(3)] for t in range(3)]

solver = Solver()

# Domain constraints: days 1-5
for t in range(3):
    for b in range(3):
        solver.add(day[t][b] >= 1, day[t][b] <= 5)

# Strict ordering within each cookie type
for t in range(3):
    solver.add(day[t][0] < day[t][1], day[t][1] < day[t][2])

# At least one batch on Monday (day 1)
solver.add(Or(*[day[t][b] == 1 for t in range(3) for b in range(3)]))

# Second batch of sugar is on Thursday (day 4)
solver.add(day[2][1] == 4)

# Second batch of oatmeal same day as first batch of peanut butter
solver.add(day[0][1] == day[1][0])

# Helper to get all models with the premise
def get_models_with_premise(s):
    models = []
    while True:
        if s.check() == unsat:
            break
        m = s.model()
        models.append(m)
        
        # Block current model
        block = []
        for t in range(3):
            for b in range(3):
                val = m.eval(day[t][b])
                if is_const(val):
                    block.append(day[t][b] != val)
                else:
                    block.append(day[t][b] != val.as_long())
        s.add(Or(block))
    return models

# Get all base models
base_models = get_models_with_premise(Solver())
for a in solver.assertions():
    base_models[-1]  # dummy to avoid using solver directly
base_solver = Solver()
for a in solver.assertions():
    base_solver.add(a)
base_models = get_models_with_premise(base_solver)

# Filter models that satisfy the premise: exists A != B with day[A][0] == day[B][2]
valid_models = []
for m in base_models:
    satisfies_premise = False
    for A in range(3):
        for B in range(3):
            if A != B:
                val_A0 = m.eval(day[A][0])
                val_B2 = m.eval(day[B][2])
                if is_const(val_A0):
                    val_A0 = val_A0.as_long()
                else:
                    val_A0 = int(str(val_A0))
                if is_const(val_B2):
                    val_B2 = val_B2.as_long()
                else:
                    val_B2 = int(str(val_B2))
                if val_A0 == val_B2:
                    satisfies_premise = True
                    break
        if satisfies_premise:
            break
    if satisfies_premise:
        valid_models.append(m)

# Evaluate each answer choice across all valid models
answer_choices = [
    "At least one batch of cookies is made on each of the five days.",
    "At least two batches of cookies are made on Wednesday.",
    "Exactly one batch of cookies is made on Monday.",
    "Exactly two batches of cookies are made on Tuesday.",
    "Exactly one batch of cookies is made on Friday."
]

# For each choice, check if it's true in ALL valid models
choice_always_true = []
for idx, choice in enumerate(answer_choices):
    always_true = True
    for m in valid_models:
        # Count batches per day
        count = [0] * 6  # index 1-5 for days Monday-Friday
        for t in range(3):
            for b in range(3):
                val = m.eval(day[t][b])
                if is_const(val):
                    d = val.as_long()
                else:
                    d = int(str(val))
                count[d] += 1
        
        # Evaluate the choice
        if idx == 0:  # At least one batch on each of five days
            cond = all(count[d] >= 1 for d in range(1, 6))
        elif idx == 1:  # At least two batches on Wednesday (day 3)
            cond = count[3] >= 2
        elif idx == 2:  # Exactly one batch on Monday (day 1)
            cond = count[1] == 1
        elif idx == 3:  # Exactly two batches on Tuesday (day 2)
            cond = count[2] == 2
        elif idx == 4:  # Exactly one batch on Friday (day 5)
            cond = count[5] == 1
        
        if not cond:
            always_true = False
            break
    
    choice_always_true.append(always_true)

# Find the choice that could be false (i.e., not always true)
answer_index_list = [idx for idx, always in enumerate(choice_always_true) if not always]

print(answer_index_list)