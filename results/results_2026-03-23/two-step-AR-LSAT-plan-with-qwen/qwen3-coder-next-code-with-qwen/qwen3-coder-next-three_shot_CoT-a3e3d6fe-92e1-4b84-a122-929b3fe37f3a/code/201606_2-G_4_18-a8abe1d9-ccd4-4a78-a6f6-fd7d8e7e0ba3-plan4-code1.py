from z3 import *

# Singer indices: 0-Kammer, 1-Lugo, 2-Trillo, 3-Waite, 4-Yoshida, 5-Zinn
singers = ["Kammer", "Lugo", "Trillo", "Waite", "Yoshida", "Zinn"]
recorded = {0, 1}  # Kammer and Lugo are recorded

# Answer choices as lists of singer names in order (position 0 to 5)
choices = [
    ["Kammer", "Trillo", "Zinn", "Waite", "Lugo", "Yoshida"],
    ["Waite", "Kammer", "Yoshida", "Zinn", "Lugo", "Trillo"],
    ["Waite", "Lugo", "Kammer", "Trillo", "Zinn", "Yoshida"],
    ["Waite", "Zinn", "Kammer", "Trillo", "Lugo", "Yoshida"],
    ["Zinn", "Yoshida", "Waite", "Lugo", "Kammer", "Trillo"]
]

# Create position mapping for each choice
def check_choice(choice):
    # Build position map: singer -> 1-indexed position
    pos = {}
    for i, singer in enumerate(choice):
        pos[singer] = i + 1
    
    # Check recording constraints
    # Fourth audition (position 4) must be unrecorded
    fourth_singer = choice[3]
    if pos[fourth_singer] == 4 and (singers.index(fourth_singer) in recorded):
        return False
    
    # Fifth audition (position 5) must be recorded
    fifth_singer = choice[4]
    if pos[fifth_singer] == 5 and (singers.index(fifth_singer) not in recorded):
        return False
    
    # Ordering constraints
    # Waite before both Kammer and Lugo
    if not (pos["Waite"] < pos["Kammer"] and pos["Waite"] < pos["Lugo"]):
        return False
    
    # Kammer before Trillo
    if not (pos["Kammer"] < pos["Trillo"]):
        return False
    
    # Zinn before Yoshida
    if not (pos["Zinn"] < pos["Yoshida"]):
        return False
    
    return True

# Check each choice
for idx, choice in enumerate(choices):
    if check_choice(choice):
        print(idx)
        break