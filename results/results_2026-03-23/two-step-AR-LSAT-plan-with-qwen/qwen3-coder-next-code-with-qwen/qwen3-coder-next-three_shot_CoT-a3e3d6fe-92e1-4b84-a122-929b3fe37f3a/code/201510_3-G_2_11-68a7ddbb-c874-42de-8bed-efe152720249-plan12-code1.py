from z3 import *

# Photographer indices: 0-Fuentes, 1-Gagnon, 2-Hue
# Section indices: 0-Lifestyle, 1-Metro, 2-Sports

# Variables for each photograph's photographer
L0, L1 = Ints('L0 L1')
M0, M1 = Ints('M0 M1')
S0, S1 = Ints('S0 S1')

solver = Solver()

# Domain constraints: each variable must be 0, 1, or 2
for var in [L0, L1, M0, M1, S0, S1]:
    solver.add(Or(var == 0, var == 1, var == 2))

# Global photographer count constraints: each photographer appears 1-3 times
counts = [0, 0, 0]
for var in [L0, L1, M0, M1, S0, S1]:
    counts[0] += If(var == 0, 1, 0)
    counts[1] += If(var == 1, 1, 0)
    counts[2] += If(var == 2, 1, 0)

solver.add(counts[0] >= 1, counts[0] <= 3)
solver.add(counts[1] >= 1, counts[1] <= 3)
solver.add(counts[2] >= 1, counts[2] <= 3)

# Lifestyle/Metro overlap constraint: at least one photographer appears in both sections
overlap_constraints = []
for p in range(3):
    overlap_constraints.append(
        And(
            Or(L0 == p, L1 == p),
            Or(M0 == p, M1 == p)
        )
    )
solver.add(Or(*overlap_constraints))

# Hue-Fuentes balance constraint: #Hue in Lifestyle = #Fuentes in Sports
hue_lifestyle = If(L0 == 2, 1, 0) + If(L1 == 2, 1, 0)
fuentes_sports = If(S0 == 0, 1, 0) + If(S1 == 0, 1, 0)
solver.add(hue_lifestyle == fuentes_sports)

# Gagnon constraint: no Gagnon photos in Sports
solver.add(S0 != 1, S1 != 1)

# Given scenario: Lifestyle has one Fuentes and one Hue
solver.add(Or(
    And(L0 == 0, L1 == 2),
    And(L0 == 2, L1 == 0)
))

# Answer choices
answer_choices = [
    And(M0 == 0, M1 == 0),  # Both Metro photos by Fuentes
    And(M0 == 1, M1 == 1),  # Both Metro photos by Gagnon
    (If(M0 == 2, 1, 0) + If(M1 == 2, 1, 0)) == 1,  # Exactly one Metro photo by Hue
    And(S0 == 2, S1 == 2),  # Both Sports photos by Hue
    And(S0 != 2, S1 != 2)   # Neither Sports photo by Hue
]

answer_index_list = []
for idx, choice in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    s_chk.add(choice)
    
    if s_chk.check() == sat:
        answer_index_list.append(idx)

print(answer_index_list)