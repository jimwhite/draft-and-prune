from z3 import *
import itertools

# Band indices: Uneasy=0, Vegemite=1, Wellspring=2, Xpert=3, Yardsign=4, Zircon=5
bands = ["Uneasy", "Vegemite", "Wellspring", "Xpert", "Yardsign", "Zircon"]

# Generate all permutations of slots (0-indexed positions, will convert to 1-indexed)
all_perms = list(itertools.permutations(range(6)))

# Function to check if a permutation satisfies original constraints
def satisfies_original(perm):
    # perm[i] = position index (0-5) for band i
    slot = [p + 1 for p in perm]  # convert to 1-indexed slots
    # Vegemite before Zircon: slot[1] < slot[5]
    if not (slot[1] < slot[5]):
        return False
    # Wellspring and Zircon before Xpert: slot[2] < slot[3] and slot[5] < slot[3]
    if not (slot[2] < slot[3] and slot[5] < slot[3]):
        return False
    # Uneasy in last three slots: slot[0] >= 4
    if not (slot[0] >= 4):
        return False
    # Yardsign in first three slots: slot[4] <= 3
    if not (slot[4] <= 3):
        return False
    return True

# Generate all solutions satisfying original constraints
original_solutions = set()
for perm in all_perms:
    if satisfies_original(perm):
        # Store as tuple of slots (1-indexed) for bands in order
        slot = [p + 1 for p in perm]
        original_solutions.add(tuple(slot))

# Function to check if a permutation satisfies both original and choice constraints
def satisfies_choice(perm, choice_idx):
    slot = [p + 1 for p in perm]
    
    # Check original constraints first
    if not satisfies_original(perm):
        return False
    
    # Add choice-specific constraints
    if choice_idx == 0:  # Only Uneasy can perform in a later slot than Xpert
        # For all bands b != Uneasy: slot[b] <= slot[Xpert]
        for b in [1, 2, 4, 5]:  # Vegemite, Wellspring, Yardsign, Zircon
            if not (slot[b] <= slot[3]):
                return False
        # Uneasy > Xpert (optional but safe to enforce for full equivalence)
        if not (slot[0] > slot[3]):
            return False
    elif choice_idx == 1:  # Vegemite < Wellspring < Zircon
        if not (slot[1] < slot[2] and slot[2] < slot[5]):
            return False
    elif choice_idx == 2:  # Vegemite and Wellspring before Xpert
        if not (slot[1] < slot[3] and slot[2] < slot[3]):
            return False
    elif choice_idx == 3:  # Xpert immediately before or after Uneasy
        if not (abs(slot[0] - slot[3]) == 1):
            return False
    elif choice_idx == 4:  # Xpert in slot 5 or 6
        if not (slot[3] == 5 or slot[3] == 6):
            return False
    
    return True

# Check each choice
answer_index_list = []
for idx in range(5):
    # Generate solutions with original + choice constraints
    choice_solutions = set()
    for perm in all_perms:
        if satisfies_choice(perm, idx):
            slot = [p + 1 for p in perm]
            choice_solutions.add(tuple(slot))
    
    # Check if solution sets are identical
    if choice_solutions == original_solutions:
        answer_index_list.append(idx)

print(answer_index_list)