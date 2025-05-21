from z3 import *

# Define variables
birds = {'O': 0, 'P': 1, 'R': 2, 'S': 3, 'T': 4}
locations = {'G': 0, 'H': 1}
bird_lecture = Array('bird_lecture', IntSort(), IntSort())
location_lecture = Array('location_lecture', IntSort(), IntSort())

solver = Solver()

# Constraint 1: Distinct Birds
solver.add(Distinct([bird_lecture[i] for i in range(1, 6)]))

# Constraint 2: Location Domain
solver.add(And([And(location_lecture[i] >= 0, location_lecture[i] <= 1) for i in range(1, 6)]))

# Constraint 3: First Lecture in Gladwyn
solver.add(location_lecture[1] == locations['G'])

# Constraint 4: Fourth Lecture in Howard
solver.add(location_lecture[4] == locations['H'])

# Constraint 5: Three Lectures in Gladwyn
solver.add(Sum([If(location_lecture[i] == locations['G'], 1, 0) for i in range(1, 6)]) == 3)

# Constraint 6: Sandpipers in Howard
solver.add(And([Implies(bird_lecture[i] == birds['S'], location_lecture[i] == locations['H']) for i in range(1, 6)]))

# Constraint 7: Sandpipers before Oystercatchers
i = Int('i')
j = Int('j')
solver.add(Exists([i, j], And(i >= 1, i <= 5, j >= 1, j <= 5, i < j, bird_lecture[i] == birds['S'], bird_lecture[j] == birds['O'])))

# Constraint 8: Terns before Petrels
i = Int('i') # Redeclare i and j for this constraint
j = Int('j')
solver.add(Exists([i, j], And(i >= 1, i <= 5, j >= 1, j <= 5, i < j, bird_lecture[i] == birds['T'], bird_lecture[j] == birds['P'])))


# Constraint 9: Petrels in Gladwyn
solver.add(And([Implies(bird_lecture[i] == birds['P'], location_lecture[i] == locations['G']) for i in range(1, 6)]))

# Constraint 10: Terns in Howard
solver.add(And([Implies(bird_lecture[i] == birds['T'], location_lecture[i] == locations['H']) for i in range(1, 6)]))

# Check answer choices
choices = [
    (birds['O'], locations['G']),  # A
    (birds['R'], locations['H']),  # B
    (birds['R'], locations['G']),  # C
    (birds['S'], locations['H']),  # D
    (birds['T'], locations['H']),  # E
]

for i, (bird, location) in enumerate(choices):
    solver.push()
    solver.add(And(bird_lecture[3] == bird, location_lecture[3] == location))
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

