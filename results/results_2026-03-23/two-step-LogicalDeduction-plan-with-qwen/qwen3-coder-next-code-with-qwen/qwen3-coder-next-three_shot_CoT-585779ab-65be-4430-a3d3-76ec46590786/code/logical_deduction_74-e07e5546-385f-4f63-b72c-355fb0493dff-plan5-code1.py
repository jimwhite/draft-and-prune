from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["Ana", "Rob", "Amy", "Dan", "Joe"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraint that all golfers have different positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Rob finished below Dan" → Rob's position > Dan's position
problem.addConstraint(lambda Rob, Dan: Rob > Dan, ["Rob", "Dan"])

# "Joe finished below Ana" → Joe's position > Ana's position
problem.addConstraint(lambda Joe, Ana: Joe > Ana, ["Joe", "Ana"])

# "Joe finished above Amy" → Joe's position < Amy's position
problem.addConstraint(lambda Joe, Amy: Joe < Amy, ["Joe", "Amy"])

# "Dan finished below Amy" → Dan's position > Amy's position
problem.addConstraint(lambda Dan, Amy: Dan > Amy, ["Dan", "Amy"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Amy",
    "D": "Dan",
    "E": "Joe"
}

# Find who finished third (position 3)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 3:
            print(letter)