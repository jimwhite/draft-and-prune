from z3 import *

# Pianist variables: 0 = Wayne, 1 = Zara
pianist = [Int(f"p_{i}") for i in range(5)]
# Type variables: 0 = modern, 1 = traditional
type_ = [Int(f"t_{i}") for i in range(5)]

# Base solver
solver = Solver()

# Domain constraints: pianist is 0 or 1, type is 0 or 1
for i in range(5):
    solver.add(pianist[i] == 0, pianist[i] == 1)
    solver.add(type_[i] == 0, type_[i] == 1)

# Fixed constraint: Solo 3 is traditional (index 2)
solver.add(type_[2] == 1)

# Exactly two traditional pieces are performed consecutively
# Enforce exactly one pair of consecutive 1s, no triplets
consecutive_pairs = [
    And(type_[0] == 1, type_[1] == 1),
    And(type_[1] == 1, type_[2] == 1),
    And(type_[2] == 1, type_[3] == 1),
    And(type_[3] == 1, type_[4] == 1)
]
solver.add(Sum([If(pair, 1, 0) for pair in consecutive_pairs]) == 1)
# No triplets
solver.add(Not(And(type_[0] == 1, type_[1] == 1, type_[2] == 1)))
solver.add(Not(And(type_[1] == 1, type_[2] == 1, type_[3] == 1)))
solver.add(Not(And(type_[2] == 1, type_[3] == 1, type_[4] == 1)))

# Solo 4 constraint: Either Wayne performs traditional or Zara performs modern
solver.add(Or(
    And(pianist[3] == 0, type_[3] == 1),
    And(pianist[3] == 1, type_[3] == 0)
))

# Non-repetition constraint: Pianist of solo 2 (index 1) ≠ pianist of solo 5 (index 4)
solver.add(pianist[1] != pianist[4])

# No traditional piece until Wayne performs at least one modern piece
# Implement as: For each position i, if all previous solos are NOT (Wayne + modern), then type[i] must be 0
# i=0: cannot be traditional (no previous solos)
solver.add(type_[0] == 0)

# i=1: if solo 0 is not (Wayne + modern), then type[1] must be 0
solver.add(Implies(
    Or(pianist[0] != 0, type_[0] != 0),
    type_[1] == 0
))

# i=2: if solos 0 and 1 are not (Wayne + modern), then type[2] must be 0
solver.add(Implies(
    And(
        Or(pianist[0] != 0, type_[0] != 0),
        Or(pianist[1] != 0, type_[1] != 0)
    ),
    type_[2] == 0
))

# i=3: if solos 0,1,2 are not (Wayne + modern), then type[3] must be 0
solver.add(Implies(
    And(
        Or(pianist[0] != 0, type_[0] != 0),
        Or(pianist[1] != 0, type_[1] != 0),
        Or(pianist[2] != 0, type_[2] != 0)
    ),
    type_[3] == 0
))

# i=4: if solos 0,1,2,3 are not (Wayne + modern), then type[4] must be 0
solver.add(Implies(
    And(
        Or(pianist[0] != 0, type_[0] != 0),
        Or(pianist[1] != 0, type_[1] != 0),
        Or(pianist[2] != 0, type_[2] != 0),
        Or(pianist[3] != 0, type_[3] != 0)
    ),
    type_[4] == 0
))

# Scenario condition: Fifth solo is Wayne performing traditional
solver.add(pianist[4] == 0)
solver.add(type_[4] == 1)

# Answer choices
answer_choices = [
    "Zara performs the first solo.",      # A: pianist[0] == 1
    "Wayne performs the second solo.",    # B: pianist[1] == 0
    "Zara performs the third solo.",      # C: pianist[2] == 1
    "The second solo is a modern piece.", # D: type_[1] == 0
    "The fourth solo is a traditional piece." # E: type_[3] == 1
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add the specific condition for this choice
    if idx == 0:  # Zara performs first solo
        s_chk.add(pianist[0] == 1)
    elif idx == 1:  # Wayne performs second solo
        s_chk.add(pianist[1] == 0)
    elif idx == 2:  # Zara performs third solo
        s_chk.add(pianist[2] == 1)
    elif idx == 3:  # Second solo is modern
        s_chk.add(type_[1] == 0)
    elif idx == 4:  # Fourth solo is traditional
        s_chk.add(type_[3] == 1)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)