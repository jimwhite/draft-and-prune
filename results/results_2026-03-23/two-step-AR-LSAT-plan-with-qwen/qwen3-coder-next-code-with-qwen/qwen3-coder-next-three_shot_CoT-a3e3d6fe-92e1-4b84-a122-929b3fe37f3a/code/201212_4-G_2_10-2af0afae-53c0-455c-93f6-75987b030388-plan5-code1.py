from z3 import *

# Witness indices: 0-Franco, 1-Garcia, 2-Hong, 3-Iturbe, 4-Jackson
FRANCO, GARCIA, HONG, ITURBE, JACKSON = range(5)

# Day variables: 0=Monday, 1=Tuesday, 2=Wednesday
witness_day = [Int(f"witness_{i}_day") for i in range(5)]

# Base solver
solver = Solver()

# Domain constraints: each witness tests on Monday, Tuesday, or Wednesday
for i in range(5):
    solver.add(Or(witness_day[i] == 0, witness_day[i] == 1, witness_day[i] == 2))

# Exactly two witnesses testify on Tuesday
solver.add(Sum([If(witness_day[i] == 1, 1, 0) for i in range(5)]) == 2)

# At least one witness testifies on Monday
solver.add(Sum([If(witness_day[i] == 0, 1, 0) for i in range(5)]) >= 1)

# Fixed constraints
solver.add(witness_day[ITURBE] == 2)  # Iturbe testifies on Wednesday
solver.add(witness_day[HONG] != 0)    # Hong does not testify on Monday

# Franco and Garcia do not testify on the same day
solver.add(witness_day[FRANCO] != witness_day[GARCIA])

# Conditional constraint: Franco and Hong testify on the same day
solver.add(witness_day[FRANCO] == witness_day[HONG])

# Answer choices (as conditions that must be true)
answer_conditions = [
    witness_day[FRANCO] == 2,                    # Franco is scheduled to testify on Wednesday
    witness_day[GARCIA] == 0,                    # Garcia is scheduled to testify on Monday
    witness_day[GARCIA] == 2,                    # Garcia is scheduled to testify on Wednesday
    witness_day[HONG] == 1,                      # Hong is scheduled to testify on Tuesday
    And(witness_day[ITURBE] == 2,                # Iturbe is the only witness scheduled to testify on Wednesday
        Sum([If(witness_day[i] == 2, 1, 0) for i in range(5)]) == 1)
]

# Check each answer choice using proof by contradiction
answer_index_list = []
for idx, cond in enumerate(answer_conditions):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Assert the negation of the answer choice
    s_chk.add(Not(cond))
    
    # If UNSAT, then the answer choice must be true
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)