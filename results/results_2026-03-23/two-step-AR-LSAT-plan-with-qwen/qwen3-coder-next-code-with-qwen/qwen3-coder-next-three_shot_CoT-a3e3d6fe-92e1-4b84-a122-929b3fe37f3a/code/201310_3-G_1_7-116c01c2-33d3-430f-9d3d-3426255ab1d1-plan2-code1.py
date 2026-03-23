from z3 import *
import itertools

# Band indices: Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]
n = len(bands)

# Generate all permutations of positions 1..6
all_perms = list(itertools.permutations(range(1, n+1)))

# Base constraints (original problem)
def satisfies_original(perm):
    pos = {bands[i]: perm[i] for i in range(n)}
    
    # Vegemite before Zircon
    if not (pos["Vegemite"] < pos["Zircon"]):
        return False
    
    # Wellspring and Zircon before Xpert
    if not (pos["Wellspring"] < pos["Xpert"] and pos["Zircon"] < pos["Xpert"]):
        return False
    
    # Uneasy in last three slots (4,5,6)
    if not (4 <= pos["Uneasy"] <= 6):
        return False
    
    # Yardsign in first three slots (1,2,3)
    if not (1 <= pos["Yardsign"] <= 3):
        return False
    
    return True

# Check each answer choice
answer_index_list = []

# Choice 0: "Only Uneasy can perform in a later slot than Xpert."
def satisfies_choice0(perm):
    pos = {bands[i]: perm[i] for i in range(n)}
    
    # Only Uneasy can be after Xpert means: if any band is after Xpert, it must be Uneasy
    # i.e., for all bands b != Uneasy: pos[b] < pos[Xpert]
    for b in bands:
        if b != "Uneasy" and not (pos[b] < pos["Xpert"]):
            return False
    # Also, Uneasy may or may not be after Xpert (not required)
    return True

# Choice 1: "Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon."
def satisfies_choice1(perm):
    pos = {bands[i]: perm[i] for i in range(n)}
    return (pos["Vegemite"] < pos["Wellspring"]) and (pos["Wellspring"] < pos["Zircon"])

# Choice 2: "Vegemite and Wellspring each perform in an earlier slot than Xpert."
def satisfies_choice2(perm):
    pos = {bands[i]: perm[i] for i in range(n)}
    return (pos["Vegemite"] < pos["Xpert"]) and (pos["Wellspring"] < pos["Xpert"])

# Choice 3: "Xpert performs either immediately before or immediately after Uneasy."
def satisfies_choice3(perm):
    pos = {bands[i]: perm[i] for i in range(n)}
    return abs(pos["Xpert"] - pos["Uneasy"]) == 1

# Choice 4: "Xpert performs in either slot five or slot six."
def satisfies_choice4(perm):
    pos = {bands[i]: perm[i] for i in range(n)}
    return pos["Xpert"] in [5, 6]

# Find all permutations satisfying original constraints
original_models = [perm for perm in all_perms if satisfies_original(perm)]

# For each answer choice, check equivalence
choices = [satisfies_choice0, satisfies_choice1, satisfies_choice2, satisfies_choice3, satisfies_choice4]

for idx, choice_func in enumerate(choices):
    # Get models satisfying the new constraint (plus other original constraints)
    choice_models = [perm for perm in all_perms if satisfies_original(perm) and choice_func(perm)]
    
    # Check 1: All original models satisfy the new constraint
    if len(choice_models) != len(original_models):
        continue
    
    # Check 2: Every model satisfying the new constraint (plus other constraints) satisfies original Wellspring/Zircon < Xpert
    # Since we already filtered by satisfies_original, this is implicitly satisfied
    
    # But we need to ensure the new constraint *replaces* the Wellspring/Zircon < Xpert constraints
    # So we need to check: models satisfying new constraint + other original constraints = models satisfying original constraints
    
    # Actually, we need to check: 
    # (a) Every model satisfying original constraints also satisfies the new constraint
    # (b) Every model satisfying the new constraint + other original constraints also satisfies Wellspring < Xpert and Zircon < Xpert
    
    # (a) is already checked by choice_models == original_models
    # For (b), we need to check that for every perm in choice_models, Wellspring < Xpert and Zircon < Xpert hold
    all_satisfy_wz = True
    for perm in choice_models:
        pos = {bands[i]: perm[i] for i in range(n)}
        if not (pos["Wellspring"] < pos["Xpert"] and pos["Zircon"] < pos["Xpert"]):
            all_satisfy_wz = False
            break
    
    if len(choice_models) == len(original_models) and all_satisfy_wz:
        answer_index_list.append(idx)

print(answer_index_list)