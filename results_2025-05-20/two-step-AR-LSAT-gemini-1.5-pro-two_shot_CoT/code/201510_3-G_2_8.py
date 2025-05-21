from z3 import *

# Define variables
N_FL = Int('N_FL')
N_FM = Int('N_FM')
N_FS = Int('N_FS')
N_GL = Int('N_GL')
N_GM = Int('N_GM')
N_GS = Int('N_GS')
N_HL = Int('N_HL')
N_HM = Int('N_HM')
N_HS = Int('N_HS')

Total_F = Int('Total_F')
Total_G = Int('Total_G')
Total_H = Int('Total_H')

solver = Solver()

# Non-negativity constraints
solver.add(N_FL >= 0, N_FM >= 0, N_FS >= 0, N_GL >= 0, N_GM >= 0, N_GS >= 0, N_HL >= 0, N_HM >= 0, N_HS >= 0)


# Section totals
solver.add(N_FL + N_GL + N_HL == 2)
solver.add(N_FM + N_GM + N_HM == 2)
solver.add(N_FS + N_GS + N_HS == 2)

# Photographer totals
solver.add(Total_F == N_FL + N_FM + N_FS)
solver.add(Total_G == N_GL + N_GM + N_GS)
solver.add(Total_H == N_HL + N_HM + N_HS)

# Photographer count range
solver.add(Total_F >= 1, Total_F <= 3)
solver.add(Total_G >= 1, Total_G <= 3)
solver.add(Total_H >= 1, Total_H <= 3)

# Lifestyle/Metro overlap
solver.add(Or(And(N_FL >= 1, N_FM >= 1), And(N_GL >= 1, N_GM >= 1), And(N_HL >= 1, N_HM >= 1)))

# Hue in L = Fuentes in S
solver.add(N_HL == N_FS)

# No Gagnon in Sports
solver.add(N_GS == 0)

# Question condition: Both Lifestyle photos are by Hue
solver.add(N_HL == 2, N_FL == 0, N_GL == 0)

# Check answer choices
answer_choices = [
    Total_F == 1,  # A
    Total_F == 3,  # B
    Total_G == 1,  # C
    Total_G == 2,  # D
    Total_H == 2   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(Not(choice))
    if solver.check() == unsat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()