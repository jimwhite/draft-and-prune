from z3 import *

# Solo positions: 0 to 4 (1-indexed: 1 to 5)
# pianist[i] = True if Wayne, False if Zara
# type[i] = True if traditional, False if modern

pianist = [Bool(f"p_{i}") for i in range(5)]
ttype = [Bool(f"t_{i}") for i in range(5)]

solver = Solver()

# Fixed constraint: third solo is traditional (index 2)
solver.add(ttype[2] == True)

# Exactly two consecutive traditional pieces
# We need exactly one pair of consecutive trues, and no triplets

# Define adjacency pairs
adjacent_pairs = [(i, i+1) for i in range(4)]

# Count number of adjacent traditional pairs
adjacent_trad_pairs = [And(ttype[i], ttype[i+1]) for i in range(4)]

# Exactly one adjacent pair of traditional pieces
solver.add(Sum([If(pair, 1, 0) for pair in adjacent_trad_pairs]) == 1)

# Ensure no three consecutive traditional pieces
for i in range(3):
    solver.add(Not(And(ttype[i], ttype[i+1], ttype[i+2])))

# Fourth solo constraint: (Wayne traditional) OR (Zara modern)
solver.add(Or(And(pianist[3] == True, ttype[3] == True), 
             And(pianist[3] == False, ttype[3] == False)))

# Pianist constraint: second solo pianist != fifth solo pianist
solver.add(pianist[1] != pianist[4])

# No traditional piece until Wayne performs at least one modern piece
# Find first traditional position and ensure there's a Wayne modern before it

# If the first solo is traditional, then no Wayne modern can precede it → impossible
solver.add(Or(ttype[0] == False, 
              And(pianist[0] == True, ttype[0] == False)))

# More robust: for each position i where type[i] is True, 
# there must exist j < i such that pianist[j] == True and type[j] == False
for i in range(5):
    if i > 0:
        # If ttype[i] is True, then there must be a Wayne modern before i
        solver.add(Implies(ttype[i] == True, 
                          Or([And(pianist[j] == True, ttype[j] == False) for j in range(i)])))
    else:
        # For i=0, if ttype[0] is True, then no Wayne modern before → impossible
        solver.add(Not(ttype[0] == True))

# Hypothetical condition: fifth solo is Wayne *traditional*
hyp_solver = Solver()
hyp_solver.add(solver.assertions())
hyp_solver.add(pianist[4] == True, ttype[4] == True)

# Answer choices
answer_choices = [
    ("Zara performs the first solo.", lambda: pianist[0] == False),
    ("Wayne performs the second solo.", lambda: pianist[1] == True),
    ("Zara performs the third solo.", lambda: pianist[2] == False),
    ("The second solo is a modern piece.", lambda: ttype[1] == False),
    ("The fourth solo is a traditional piece.", lambda: ttype[3] == True)
]

# Check each answer choice
answer_index_list = []
for idx, (desc, constraint) in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(hyp_solver.assertions())
    s_chk.add(constraint())
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)