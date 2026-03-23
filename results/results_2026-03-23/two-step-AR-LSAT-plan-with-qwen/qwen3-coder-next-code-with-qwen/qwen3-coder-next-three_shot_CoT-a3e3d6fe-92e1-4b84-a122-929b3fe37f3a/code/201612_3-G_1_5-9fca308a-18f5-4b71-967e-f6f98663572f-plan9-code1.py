from z3 import *

# Student indices: Juana=0, Kelly=1, Lateefah=2, Mei=3, Olga=4
team = [Int(f"team_{i}") for i in range(5)]
facilitator = [Bool(f"facilitator_{i}") for i in range(5)]

solver = Solver()

# Team size constraints: one team has 2 members, the other has 3
count_green = Sum([If(team[i] == 0, 1, 0) for i in range(5)])
solver.add(Or(count_green == 2, count_green == 3))

# Fixed team assignments
solver.add(team[2] == 0)  # Lateefah is on green team
solver.add(team[4] != team[0])  # Juana and Olga on different teams

# Facilitator constraints: exactly one per team
green_facilitators = [And(team[i] == 0, facilitator[i]) for i in range(5)]
red_facilitators = [And(team[i] == 1, facilitator[i]) for i in range(5)]
solver.add(PbEq([(green_facilitators[i], 1) for i in range(5)], 1))
solver.add(PbEq([(red_facilitators[i], 1) for i in range(5)], 1))

# Given facilitator constraints
solver.add(facilitator[4] == True)  # Olga is a facilitator
solver.add(facilitator[1] == False)  # Kelly is not a facilitator

# Premise: Mei is on green team
solver.add(team[3] == 0)

# Answer choices as formulas (to be checked for necessity)
answer_formulas = [
    team[0] == 0,                    # A: Juana is on green team
    team[1] == 1,                    # B: Kelly is on red team
    team[4] == 0,                    # C: Olga is on green team
    And(team[2] == 0, facilitator[2]), # D: Lateefah is a facilitator
    And(team[3] == 0, facilitator[3])  # E: Mei is a facilitator
]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, formula in enumerate(answer_formulas):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert that the answer choice is false
    s_chk.add(Not(formula))
    
    # If UNSAT, the formula must be true (i.e., this is a necessary condition)
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

# Print the index of the forced answer (should be exactly one)
print(answer_index_list[0] if len(answer_index_list) == 1 else answer_index_list)