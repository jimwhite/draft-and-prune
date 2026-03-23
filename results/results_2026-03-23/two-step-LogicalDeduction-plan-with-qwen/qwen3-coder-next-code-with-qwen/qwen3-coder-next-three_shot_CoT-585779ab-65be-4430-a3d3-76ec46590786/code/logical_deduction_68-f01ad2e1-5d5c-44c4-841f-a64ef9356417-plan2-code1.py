from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place, 5 = last)
golfers = ["Mel", "Dan", "Amy", "Joe", "Eve"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# "Amy finished below Dan" -> Amy's position > Dan's position
problem.addConstraint(lambda amy, dan: amy > dan, ["Amy", "Dan"])

# "Mel finished first" -> Mel's position = 1
problem.addConstraint(lambda mel: mel == 1, ["Mel"])

# "Joe finished above Dan" -> Joe's position < Dan's position
problem.addConstraint(lambda joe, dan: joe < dan, ["Joe", "Dan"])

# "Eve finished last" -> Eve's position = 5
problem.addConstraint(lambda eve: eve == 5, ["Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfer names
choices = {
    "A": "Mel",
    "B": "Dan",
    "C": "Amy",
    "D": "Joe",
    "E": "Eve"
}

# Find which golfer is in position 5 (last) and print the corresponding choice letter
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)