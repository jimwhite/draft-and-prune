from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 5=last)
golfers = ["Mel", "Dan", "Amy", "Joe", "Eve"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Amy finished below Dan" → Amy's position > Dan's position
problem.addConstraint(lambda amy, dan: amy > dan, ["Amy", "Dan"])

# "Mel finished first" → Mel's position = 1
problem.addConstraint(lambda mel: mel == 1, ["Mel"])

# "Joe finished above Dan" → Joe's position < Dan's position
problem.addConstraint(lambda joe, dan: joe < dan, ["Joe", "Dan"])

# "Eve finished last" → Eve's position = 5
problem.addConstraint(lambda eve: eve == 5, ["Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Mel",
    "B": "Dan",
    "C": "Amy",
    "D": "Joe",
    "E": "Eve"
}

# Find which golfer finished last (position 5)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 5:
            print(letter)