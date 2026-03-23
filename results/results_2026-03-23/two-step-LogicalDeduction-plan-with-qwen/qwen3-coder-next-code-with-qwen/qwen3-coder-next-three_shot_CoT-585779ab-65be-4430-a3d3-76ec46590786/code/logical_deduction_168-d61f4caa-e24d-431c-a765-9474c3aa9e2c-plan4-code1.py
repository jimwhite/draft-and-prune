from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first, 7 = last)
golfers = ["Ada", "Ana", "Rob", "Amy", "Dan", "Joe", "Eli"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Eli finished below Amy" → Eli's position > Amy's position
problem.addConstraint(lambda Eli, Amy: Eli > Amy, ["Eli", "Amy"])

# "Ada finished third" → Ada's position = 3
problem.addConstraint(lambda Ada: Ada == 3, ["Ada"])

# "Amy finished below Rob" → Amy's position > Rob's position
problem.addConstraint(lambda Amy, Rob: Amy > Rob, ["Amy", "Rob"])

# "Dan finished last" → Dan's position = 7
problem.addConstraint(lambda Dan: Dan == 7, ["Dan"])

# "Rob finished second" → Rob's position = 2
problem.addConstraint(lambda Rob: Rob == 2, ["Rob"])

# "Ana finished fourth" → Ana's position = 4
problem.addConstraint(lambda Ana: Ana == 4, ["Ana"])

# Solve the problem
solutions = problem.getSolutions()

# Since there's only one solution, get it
solution = solutions[0]

# The question asks who finished last (position 7)
# According to the constraints, Dan must be at position 7
# Let's verify and output the correct choice

# Map choices to golfers
choices = {
    "A": "Ada",
    "B": "Ana",
    "C": "Rob",
    "D": "Amy",
    "E": "Dan",
    "F": "Joe",
    "G": "Eli"
}

# Find who has position 7
for letter, golfer in choices.items():
    if solution[golfer] == 7:
        print(letter)