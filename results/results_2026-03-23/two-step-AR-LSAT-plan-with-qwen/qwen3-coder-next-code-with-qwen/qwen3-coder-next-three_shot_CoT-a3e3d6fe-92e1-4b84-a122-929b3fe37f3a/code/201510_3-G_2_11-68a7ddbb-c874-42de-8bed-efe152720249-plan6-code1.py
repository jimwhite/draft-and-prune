from z3 import *

# Photographer indices: 0-Fuentes, 1-Gagnon, 2-Hue
# Section indices: 0-Lifestyle, 1-Metro, 2-Sports

# Create count variables: count[section][photographer]
count = [[Int(f"count_{s}_{p}") for p in range(3)] for s in range(3)]

# Base solver
solver = Solver()

# Section size constraints: each section has exactly 2 photos
for s in range(3):
    solver.add(sum(count[s][p] for p in range(3)) == 2)

# Photographer total constraints: each photographer appears 1-3 times
for p in range(3):
    total = sum(count[s][p] for s in range(3))
    solver.add(total >= 1, total <= 3)

# Gagnon constraint: no Gagnon photos in Sports section
solver.add(count[2][1] == 0)

# Lifestyle-Metro overlap constraint: at least one photographer appears in both
overlap_constraint = Or(
    And(count[0][0] > 0, count[1][0] > 0),
    And(count[0][1] > 0, count[1][1] > 0),
    And(count[0][2] > 0, count[1][2] > 0)
)
solver.add(overlap_constraint)

# Hue-Fuentes balance constraint: count[Lifestyle][Hue] == count[Sports][Fuentes]
solver.add(count[0][2] == count[2][0])

# Given condition: Lifestyle has exactly one Fuentes and one Hue
solver.add(count[0][0] == 1, count[0][2] == 1)
# Implicit: Lifestyle has exactly two photos, so Gagnon count in Lifestyle is 0
solver.add(count[0][1] == 0)

# Domain constraints for counts (non-negative integers)
for s in range(3):
    for p in range(3):
        solver.add(count[s][p] >= 0)

# Answer choices
answer_choices = [
    "Metro both Fuentes",      # A: count[Metro][Fuentes] == 2
    "Metro both Gagnon",       # B: count[Metro][Gagnon] == 2
    "Metro exactly one Hue",   # C: count[Metro][Hue] == 1
    "Sports both Hue",         # D: count[Sports][Hue] == 2
    "Sports neither Hue"       # E: count[Sports][Hue] == 0
]

# Check each answer choice
answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    if choice == "Metro both Fuentes":
        # count[Metro][Fuentes] == 2, so Metro: [2,0,0]
        s_chk.add(count[1][0] == 2)
    elif choice == "Metro both Gagnon":
        # count[Metro][Gagnon] == 2, so Metro: [0,2,0]
        s_chk.add(count[1][1] == 2)
    elif choice == "Metro exactly one Hue":
        # count[Metro][Hue] == 1
        s_chk.add(count[1][2] == 1)
    elif choice == "Sports both Hue":
        # count[Sports][Hue] == 2
        s_chk.add(count[2][2] == 2)
    elif choice == "Sports neither Hue":
        # count[Sports][Hue] == 0
        s_chk.add(count[2][2] == 0)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)