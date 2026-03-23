from z3 import *

# Photographer indices: 0=Frost, 1=Gonzalez, 2=Heideck, 3=Knutson, 4=Lai, 5=Mays
photographers = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

# Define the five answer choices as assignments:
# Each assignment is a list where index i gives: 1=Silva, 2=Thorne, 0=unassigned
choices = [
    # Choice 0: 'Silva University: Gonzalez, Lai Thorne University: Frost, Heideck, Mays'
    [2, 1, 2, 0, 1, 2],  # Frost=Thorne(2), Gonzalez=Silva(1), Heideck=Thorne(2), Knutson=unassigned(0), Lai=Silva(1), Mays=Thorne(2)
    # Choice 1: 'Silva University: Gonzalez, Mays Thorne University: Knutson, Lai'
    [0, 1, 0, 2, 2, 1],  # Frost=unassigned(0), Gonzalez=Silva(1), Heideck=unassigned(0), Knutson=Thorne(2), Lai=Thorne(2), Mays=Silva(1)
    # Choice 2: 'Silva University: Frost, Gonzalez, Heideck Thorne University: Knutson, Lai, Mays'
    [1, 1, 1, 2, 2, 2],  # Frost=Silva(1), Gonzalez=Silva(1), Heideck=Silva(1), Knutson=Thorne(2), Lai=Thorne(2), Mays=Thorne(2)
    # Choice 3: 'Silva University: Frost, Heideck, Mays Thorne University: Gonzalez, Lai'
    [1, 2, 1, 0, 2, 1],  # Frost=Silva(1), Gonzalez=Thorne(2), Heideck=Silva(1), Knutson=unassigned(0), Lai=Thorne(2), Mays=Silva(1)
    # Choice 4: 'Silva University: Frost, Heideck, Mays Thorne University: Gonzalez, Knutson, Lai'
    [1, 2, 1, 2, 2, 1]   # Frost=Silva(1), Gonzalez=Thorne(2), Heideck=Silva(1), Knutson=Thorne(2), Lai=Thorne(2), Mays=Silva(1)
]

# Constraints function
def check_constraints(assignment):
    # assignment: list of 6 integers (0=unassigned, 1=Silva, 2=Thorne)
    
    # Extract assignments
    F = assignment[0]  # Frost
    G = assignment[1]  # Gonzalez
    H = assignment[2]  # Heideck
    K = assignment[3]  # Knutson
    L = assignment[4]  # Lai
    M = assignment[5]  # Mays
    
    # Constraint 1: Frost and Heideck must be assigned together to the same ceremony
    if (F != 0 or H != 0) and F != H:
        return False
    
    # Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
    if L != 0 and M != 0 and L == M:
        return False
    
    # Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
    if G == 1 and L != 2:
        return False
    
    # Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
    if K != 2:  # Knutson is not at Thorne (either Silva or unassigned)
        if H != 2 or M != 2:
            return False
    
    # Constraint 5: Each ceremony must have at least two photographers assigned
    silva_count = sum(1 for x in assignment if x == 1)
    thorne_count = sum(1 for x in assignment if x == 2)
    
    if silva_count < 2 or thorne_count < 2:
        return False
    
    return True

# Check each choice
for idx, assignment in enumerate(choices):
    if check_constraints(assignment):
        print(idx)
        break