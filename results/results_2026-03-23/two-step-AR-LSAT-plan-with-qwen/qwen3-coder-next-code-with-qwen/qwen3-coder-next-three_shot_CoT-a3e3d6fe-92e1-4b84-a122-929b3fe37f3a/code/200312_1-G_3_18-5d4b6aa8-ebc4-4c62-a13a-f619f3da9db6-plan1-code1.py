from z3 import *

# Cookie types: 0=oatmeal, 1=peanut butter, 2=sugar
# Batch numbers: 1, 2, 3 (we'll use indices 0,1,2 for batch numbers internally)
# Days: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri

# day[c][b] = day on which batch b+1 of cookie type c is made
day = [[Int(f"day_{c}_{b}") for b in range(3)] for c in range(3)]

solver = Solver()

# Domain constraints: each day between 0 and 4
for c in range(3):
    for b in range(3):
        solver.add(day[c][b] >= 0, day[c][b] <= 4)

# Distinct-per-type constraints: for each cookie type, batches on different days
for c in range(3):
    solver.add(day[c][0] != day[c][1], day[c][0] != day[c][2], day[c][1] != day[c][2])

# At least one batch on Monday (day 0)
solver.add(Or(*[day[c][b] == 0 for c in range(3) for b in range(3)]))

# Oatmeal-2 = Peanut Butter-1: day[0][1] == day[1][0]
solver.add(day[0][1] == day[1][0])

# Sugar-2 = Thursday: day[2][1] == 3
solver.add(day[2][1] == 3)

# Premise: one kind's first batch is made on same day as another kind's third batch
# We'll create a separate solver for the premise condition
premise_solvers = []
for c1 in range(3):
    for c2 in range(3):
        if c1 != c2:
            s = Solver()
            s.add(solver.assertions())
            # First batch of c1 (day[c1][0]) == third batch of c2 (day[c2][2])
            s.add(day[c1][0] == day[c2][2])
            premise_solvers.append(s)

# For each answer choice, check if it could be false (i.e., there exists a model satisfying premise where the statement is false)
answer_index_list = []

# Choice 0: At least one batch on each of the five days
def choice0_condition():
    return And(*[Or(*[day[c][b] == d for c in range(3) for b in range(3)]) for d in range(5)])

def choice0_negation():
    return Not(choice0_condition())

# Choice 1: At least two batches on Wednesday (day=2)
def choice1_condition():
    return Sum([If(day[c][b] == 2, 1, 0) for c in range(3) for b in range(3)]) >= 2

def choice1_negation():
    return Not(choice1_condition())

# Choice 2: Exactly one batch on Monday (day=0)
def choice2_condition():
    return Sum([If(day[c][b] == 0, 1, 0) for c in range(3) for b in range(3)]) == 1

def choice2_negation():
    return Not(choice2_condition())

# Choice 3: Exactly two batches on Tuesday (day=1)
def choice3_condition():
    return Sum([If(day[c][b] == 1, 1, 0) for c in range(3) for b in range(3)]) == 2

def choice3_negation():
    return Not(choice3_condition())

# Choice 4: Exactly one batch on Friday (day=4)
def choice4_condition():
    return Sum([If(day[c][b] == 4, 1, 0) for c in range(3) for b in range(3)]) == 1

def choice4_negation():
    return Not(choice4_condition())

# Check each choice
for idx, negation_func in enumerate([choice0_negation(), choice1_negation(), choice2_negation(), choice3_negation(), choice4_negation()]):
    found_sat = False
    for s in premise_solvers:
        s_check = Solver()
        s_check.add(s.assertions())
        s_check.add(negation_func)
        
        if s_check.check() == sat:
            found_sat = True
            break
    
    if found_sat:
        answer_index_list.append(idx)

print(answer_index_list)