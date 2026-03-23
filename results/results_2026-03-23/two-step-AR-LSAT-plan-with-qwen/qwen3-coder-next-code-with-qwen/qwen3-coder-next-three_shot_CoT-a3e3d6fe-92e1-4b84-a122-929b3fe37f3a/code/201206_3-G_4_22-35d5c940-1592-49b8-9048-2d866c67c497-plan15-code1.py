from z3 import *

# Solo positions: 0 to 4 (1st to 5th)
p = [Bool(f"p_{i}") for i in range(5)]  # True if Wayne performs solo i
t = [Bool(f"t_{i}") for i in range(5)]  # True if solo i is traditional

solver = Solver()

# Third solo is traditional
solver.add(t[2])

# Exactly one pair of consecutive traditional solos, no three in a row
# Enumerate all valid t patterns with exactly one adjacent pair and t[2]=True
valid_t_patterns = [
    [False, True, True, False, False],  # pair at (1,2)
    [True, True, False, False, True],   # pair at (0,1), isolated at 4
    [False, True, True, False, True],   # pair at (1,2), isolated at 4
    [False, False, True, True, False]   # pair at (2,3)
]

# Add disjunction of valid patterns
pattern_constraints = []
for pattern in valid_t_patterns:
    conj = And(*[t[i] == pattern[i] for i in range(5)])
    pattern_constraints.append(conj)
solver.add(Or(*pattern_constraints))

# Hypothesis: fifth solo Wayne performs traditional piece
solver.add(p[4], t[4])

# Fourth solo constraint: t[3] == p[3]
solver.add(t[3] == p[3])

# Pianist constraint: solo 2 pianist ≠ solo 5 pianist
solver.add(p[1] != p[4])

# No traditional piece until Wayne performs at least one modern piece
# First tradtional must be preceded by Wayne-modern
# Since t[2]=True and we have valid patterns, enforce for each pattern:
# Pattern 0: [F,T,T,F,F] → first tradtional at index 1, need p[0]=True & t[0]=False
# Pattern 2: [F,T,T,F,T] → first tradtional at index 1, need p[0]=True & t[0]=False
# Pattern 3: [F,F,T,T,F] → first tradtional at index 2, need (p[0]=True & t[0]=False) or (p[1]=True & t[1]=False)
# Pattern 1: [T,T,F,F,T] → first tradtional at index 0 → invalid (no prior solo)
# So exclude pattern 1 and enforce constraints for others

# Exclude pattern with first tradtional at index 0
solver.add(Not(And(t[0], t[1])))

# Enforce Wayne-modern before first tradtional
# For patterns where first tradtional at index 1: need p[0] & !t[0]
# For patterns where first tradtional at index 2: need (p[0] & !t[0]) or (p[1] & !t[1])
# Since t[2]=True, first tradtional ≤ 2
# If t[0]=False and t[1]=False, first tradtional=2 → need (p[0] & !t[0]) or (p[1] & !t[1])
# If t[1]=True, first tradtional=1 → need p[0] & !t[0]
# Combine: (t[0] => False) and ((t[1] & p[0]) | (!t[1] & (p[0] | p[1])))
# Simpler: enforce that before first tradtional, there's Wayne-modern
# Since only 5 solos, check cases:
# We know t[2]=True. Cases:
#   Case 1: t[0]=False, t[1]=True → need p[0] & !t[0]
#   Case 2: t[0]=False, t[1]=False → need (p[0] & !t[0]) or (p[1] & !t[1])
#   Case 3: t[0]=True → invalid (first tradtional at 0)
# So:
solver.add(Implies(t[1], And(Not(t[0]), p[0])))
solver.add(Implies(And(Not(t[0]), Not(t[1])), Or(And(p[0], Not(t[0])), And(p[1], Not(t[1])))))

# Answer choices
answer_choices = [
    ("Zara performs the first solo.", Not(p[0])),
    ("Wayne performs the second solo.", p[1]),
    ("Zara performs the third solo.", Not(p[2])),
    ("The second solo is a modern piece.", Not(t[1])),
    ("The fourth solo is a traditional piece.", t[3])
]

answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(constraint)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)