from z3 import *

# Days: Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
# Cookie types: O=oatmeal, P=peanut butter, S=sugar

# Create variables for each batch day
first_O = Int('first_O')
second_O = Int('second_O')
third_O = Int('third_O')
first_P = Int('first_P')
second_P = Int('second_P')
third_P = Int('third_P')
first_S = Int('first_S')
second_S = Int('second_S')
third_S = Int('third_S')

# All variables
batches = [first_O, second_O, third_O, first_P, second_P, third_P, first_S, second_S, third_S]

# Base solver
solver = Solver()

# Domain constraints: all days in [0,4]
for var in batches:
    solver.add(var >= 0, var <= 4)

# Per-type ordering constraints: first < second < third
solver.add(first_O < second_O, second_O < third_O)
solver.add(first_P < second_P, second_P < third_P)
solver.add(first_S < second_S, second_S < third_S)

# Fixed constraint: second_S == 3 (Thursday)
solver.add(second_S == 3)

# At least one batch on Monday
solver.add(Or(*[var == 0 for var in batches]))

# Cross-type constraint: second_O == first_P
solver.add(second_O == first_P)

# Premise constraint: there exists X,Y such that first_X == third_Y
premise = Or(
    first_O == third_P,
    first_O == third_S,
    first_P == third_O,
    first_P == third_S,
    first_S == third_O,
    first_S == third_P
)

# Answer choices (statements about daily batch counts)
# We'll encode each choice as a statement, then check if it *could be false* under the premise

# Helper: count batches on a given day
def count_on_day(day_val):
    return Sum([If(var == day_val, 1, 0) for var in batches])

# Monday count
cnt_Mon = count_on_day(0)
# Tuesday count
cnt_Tue = count_on_day(1)
# Wednesday count
cnt_Wed = count_on_day(2)
# Thursday count
cnt_Thu = count_on_day(3)
# Friday count
cnt_Fri = count_on_day(4)

# Define each choice statement (as a boolean expression)
choice_statements = [
    # 0: At least one batch of cookies is made on each of the five days.
    And(cnt_Mon > 0, cnt_Tue > 0, cnt_Wed > 0, cnt_Thu > 0, cnt_Fri > 0),
    # 1: At least two batches of cookies are made on Wednesday.
    cnt_Wed >= 2,
    # 2: Exactly one batch of cookies is made on Monday.
    cnt_Mon == 1,
    # 3: Exactly two batches of cookies are made on Tuesday.
    cnt_Tue == 2,
    # 4: Exactly one batch of cookies is made on Friday.
    cnt_Fri == 1
]

# Check each choice: if the statement could be false under the premise
answer_index_list = []
for idx, stmt in enumerate(choice_statements):
    s_chk = Solver()
    # Add base constraints + premise
    s_chk.add(solver.assertions())
    s_chk.add(premise)
    
    # Assert the negation of the statement
    s_chk.add(Not(stmt))
    
    if s_chk.check() == sat:
        # This statement could be false under the premise
        answer_index_list.append(idx)

print(answer_index_list)