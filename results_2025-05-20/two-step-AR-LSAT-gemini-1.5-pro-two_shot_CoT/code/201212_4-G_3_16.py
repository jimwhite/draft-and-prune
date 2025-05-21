from z3 import *

# Variables
target_times = Array('target_times', IntSort(), ArraySort(IntSort(), IntSort())) # Corrected: Declare as 2D array

# Solver
solver = Solver()

# Constraint 1: Domain of Target Times
client = Int('client')
request_type = Int('request_type')
solver.add(ForAll([client, request_type], Implies(And(client >= 0, client <= 2, request_type >= 0, request_type <= 1), And(target_times[client][request_type] >= 1, target_times[client][request_type] <= 3))))

# Constraint 2: Website Target <= Voicemail Target
client = Int('client')
solver.add(ForAll([client], Implies(And(client >= 0, client <= 2), target_times[client][0] <= target_times[client][1])))

# Constraint 3: Image Voicemail < Other Voicemails
client = Int('client')
solver.add(ForAll([client], Implies(And(client >= 1, client <= 2), target_times[0][1] < target_times[client][1])))

# Constraint 4: Solide Website < Truvest Website
solver.add(target_times[1][0] < target_times[2][0])

# Constraint 5: No Website Target is 2 days
client = Int('client')
solver.add(ForAll([client], Implies(And(client >= 0, client <= 2), target_times[client][0] != 2)))

# Answer Choices
options = [
    target_times[0][0] < target_times[1][0],  # A
    target_times[1][0] < target_times[0][0],  # B
    target_times[1][1] < target_times[2][1],  # C
    target_times[2][0] < target_times[0][0],  # D
    target_times[2][1] < target_times[1][1]   # E
]

for i, option in enumerate(options):
    solver.push()
    solver.add(option)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()
