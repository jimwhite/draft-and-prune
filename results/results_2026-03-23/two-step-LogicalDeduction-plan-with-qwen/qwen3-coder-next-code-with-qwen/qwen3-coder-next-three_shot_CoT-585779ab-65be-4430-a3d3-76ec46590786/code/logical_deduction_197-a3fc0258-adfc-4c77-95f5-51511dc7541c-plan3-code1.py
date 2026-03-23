from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Mel", "Rob", "Eli", "Dan", "Ana", "Ada", "Mya"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Ana finished last (position 7)
problem.addConstraint(lambda Ana: Ana == 7, ["Ana"])

# Rob finished fourth (position 4)
problem.addConstraint(lambda Rob: Rob == 4, ["Rob"])

# Eli finished second (position 2)
problem.addConstraint(lambda Eli: Eli == 2, ["Eli"])

# Mya finished above Rob (Mya < Rob)
problem.addConstraint(lambda Mya, Rob: Mya < Rob, ["Mya", "Rob"])

# Dan finished above Mya (Dan < Mya)
problem.addConstraint(lambda Dan, Mya: Dan < Mya, ["Dan", "Mya"])

# Mel finished above Ada (Mel < Ada)
problem.addConstraint(lambda Mel, Ada: Mel < Ada, ["Mel", "Ada"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    'A': 'Mel',
    'B': 'Rob',
    'C': 'Eli',
    'D': 'Dan',
    'E': 'Ana',
    'F': 'Ada',
    'G': 'Mya'
}

# Find which golfer finished third (position 3)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 3:
            print(letter)