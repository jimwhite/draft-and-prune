from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1-7, where 1 is first place)
golfers = ["Ada", "Ana", "Rob", "Amy", "Dan", "Joe", "Eli"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# "Eli finished below Amy" → Amy's rank < Eli's rank
problem.addConstraint(lambda Amy, Eli: Amy < Eli, ["Amy", "Eli"])

# "Ada finished third" → Ada's position == 3
problem.addConstraint(lambda Ada: Ada == 3, ["Ada"])

# "Amy finished below Rob" → Rob's rank < Amy's rank
problem.addConstraint(lambda Rob, Amy: Rob < Amy, ["Rob", "Amy"])

# "Dan finished last" → Dan's position == 7
problem.addConstraint(lambda Dan: Dan == 7, ["Dan"])

# "Rob finished second" → Rob's position == 2
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# "Ana finished fourth" → Ana's position == 4
problem.addConstraint(lambda Ana: Ana == 4, ["Ana"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Ada",
    "B": "Ana",
    "C": "Rob",
    "D": "Amy",
    "E": "Dan",
    "F": "Joe",
    "G": "Eli"
}

# Find which golfer finished last (position 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)