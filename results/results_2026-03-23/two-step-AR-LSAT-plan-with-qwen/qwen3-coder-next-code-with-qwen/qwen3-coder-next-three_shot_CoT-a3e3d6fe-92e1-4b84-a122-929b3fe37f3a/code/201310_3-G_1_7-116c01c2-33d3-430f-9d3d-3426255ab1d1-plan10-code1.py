from itertools import permutations

# Band indices: 0=Uneasy, 1=Vegemite, 2=Wellspring, 3=Xpert, 4=Yardsign, 5=Zircon
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Original constraints (including the two Xpert precedences)
def satisfies_original(perm):
    # perm is a tuple of positions for bands in order: [Uneasy, Vegemite, Wellspring, Xpert, Yardsign, Zircon]
    pos = {bands[i]: perm[i] for i in range(6)}
    
    # Vegemite < Zircon
    if not (pos["Vegemite"] < pos["Zircon"]):
        return False
    
    # Wellspring < Xpert and Zircon < Xpert
    if not (pos["Wellspring"] < pos["Xpert"] and pos["Zircon"] < pos["Xpert"]):
        return False
    
    # Uneasy in last three slots (positions 4,5,6)
    if not (pos["Uneasy"] >= 4):
        return False
    
    # Yardsign in first three slots (positions 1,2,3)
    if not (pos["Yardsign"] <= 3):
        return False
    
    return True

# Generate all original models (permutations satisfying original constraints)
original_models = []
for perm in permutations(range(1, 7)):
    if satisfies_original(perm):
        original_models.append(set(perm))

# Convert to set of tuples for comparison
original_model_set = {tuple(p) for p in original_models}

# Function to check if a candidate replacement constraint yields the same model set
def check_candidate(replacement_func):
    # Generate models satisfying original constraints EXCEPT Wellspring < Xpert and Zircon < Xpert,
    # but satisfying the replacement constraint
    candidate_models = []
    for perm in permutations(range(1, 7)):
        pos = {bands[i]: perm[i] for i in range(6)}
        
        # Check original constraints except the two Xpert precedences
        if not (pos["Vegemite"] < pos["Zircon"]):
            continue
        if not (pos["Uneasy"] >= 4):
            continue
        if not (pos["Yardsign"] <= 3):
            continue
        
        # Check replacement constraint
        if not replacement_func(pos):
            continue
            
        candidate_models.append(perm)
    
    return {tuple(m) for m in candidate_models}

# Define replacement constraints
def choice0(pos):
    # "Only Uneasy can perform in a later slot than Xpert"
    # i.e., for all bands b != Uneasy: pos[b] < pos[Xpert], and pos[Uneasy] > pos[Xpert]
    for band in ["Vegemite", "Wellspring", "Yardsign", "Zircon"]:
        if not (pos[band] < pos["Xpert"]):
            return False
    return pos["Uneasy"] > pos["Xpert"]

def choice1(pos):
    # "Vegemite < Wellspring < Zircon"
    return pos["Vegemite"] < pos["Wellspring"] and pos["Wellspring"] < pos["Zircon"]

def choice2(pos):
    # "Vegemite and Wellspring each perform in an earlier slot than Xpert"
    return pos["Vegemite"] < pos["Xpert"] and pos["Wellspring"] < pos["Xpert"]

def choice3(pos):
    # "Xpert performs either immediately before or immediately after Uneasy"
    return abs(pos["Xpert"] - pos["Uneasy"]) == 1

def choice4(pos):
    # "Xpert performs in either slot five or slot six"
    return pos["Xpert"] == 5 or pos["Xpert"] == 6

# Check each choice
answer_index_list = []
replacement_funcs = [choice0, choice1, choice2, choice3, choice4]

for idx, func in enumerate(replacement_funcs):
    candidate_model_set = check_candidate(func)
    if original_model_set == candidate_model_set:
        answer_index_list.append(idx)

print(answer_index_list)