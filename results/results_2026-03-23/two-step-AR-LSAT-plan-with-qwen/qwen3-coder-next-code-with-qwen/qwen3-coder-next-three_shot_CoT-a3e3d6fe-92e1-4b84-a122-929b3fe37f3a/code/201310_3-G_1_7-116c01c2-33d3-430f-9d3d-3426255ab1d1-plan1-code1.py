from z3 import *

# Band indices: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver with original constraints
solverA = Solver()

# Domain constraints: positions 1-6, all distinct
for i in range(6):
    solverA.add(pos[i] >= 1, pos[i] <= 6)
solverA.add(Distinct(pos))

# Original constraints
solverA.add(pos[1] < pos[5])  # Vegemite before Zircon
solverA.add(pos[2] < pos[3])  # Wellspring before Xpert
solverA.add(pos[5] < pos[3])  # Zircon before Xpert
solverA.add(pos[0] >= 4)      # Uneasy in last three slots (4,5,6)
solverA.add(pos[4] <= 3)      # Yardsign in first three slots (1,2,3)

# Answer choice constraints
# Option 0: Only Uneasy can perform in a later slot than Xpert
# i.e., for all b != 0, pos[b] < pos[3]
option0 = And(*[pos[b] < pos[3] for b in range(6) if b != 0])

# Option 1: Vegemite before Wellspring, which before Zircon
option1 = And(pos[1] < pos[2], pos[2] < pos[5])

# Option 2: Vegemite and Wellspring each before Xpert
option2 = And(pos[1] < pos[3], pos[2] < pos[3])

# Option 3: Xpert immediately before or after Uneasy
option3 = Or(pos[3] == pos[0] + 1, pos[3] == pos[0] - 1)

# Option 4: Xpert in slot five or six
option4 = Or(pos[3] == 5, pos[3] == 6)

answer_options = [option0, option1, option2, option3, option4]

# Negations of answer options
neg_option0 = Or(*[pos[b] >= pos[3] for b in range(6) if b != 0])
neg_option1 = Or(pos[1] >= pos[2], pos[2] >= pos[5])
neg_option2 = Or(pos[1] >= pos[3], pos[2] >= pos[3])
neg_option3 = And(pos[3] != pos[0] + 1, pos[3] != pos[0] - 1)
neg_option4 = And(pos[3] != 5, pos[3] != 6)

neg_options = [neg_option0, neg_option1, neg_option2, neg_option3, neg_option4]

# Original WZ constraints (Wellspring and Zircon before Xpert)
original_WZ = And(pos[2] < pos[3], pos[5] < pos[3])
neg_original_WZ = Or(pos[2] >= pos[3], pos[5] >= pos[3])

answer_index_list = []

for i in range(5):
    # Test A: Is there a model satisfying original constraints that violates answer i?
    solverA_neg_i = Solver()
    solverA_neg_i.add(solverA.assertions())
    solverA_neg_i.add(neg_options[i])
    
    # Test B: Is there a model satisfying answer i + other constraints that violates original WZ?
    solverB_i = Solver()
    # Add all original constraints except WZ
    solverB_i.add(pos[1] < pos[5])  # Vegemite before Zircon
    solverB_i.add(pos[0] >= 4)      # Uneasy in last three
    solverB_i.add(pos[4] <= 3)      # Yardsign in first three
    solverB_i.add(Distinct(pos))
    for j in range(6):
        solverB_i.add(pos[j] >= 1, pos[j] <= 6)
    # Add answer i constraint
    solverB_i.add(answer_options[i])
    
    solverB_i_neg_original = Solver()
    solverB_i_neg_original.add(solverB_i.assertions())
    solverB_i_neg_original.add(neg_original_WZ)
    
    # Check both tests
    test_A = solverA_neg_i.check() == sat
    test_B = solverB_i_neg_original.check() == sat
    
    # If both tests are UNSAT, answer i is logically equivalent
    if not test_A and not test_B:
        answer_index_list.append(i)

print(answer_index_list)