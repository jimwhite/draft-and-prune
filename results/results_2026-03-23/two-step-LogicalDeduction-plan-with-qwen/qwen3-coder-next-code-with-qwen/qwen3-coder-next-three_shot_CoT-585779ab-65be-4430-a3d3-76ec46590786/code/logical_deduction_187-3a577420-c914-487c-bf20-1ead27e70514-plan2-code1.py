from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 = first place, 7 = last)
golfers = ["Eve", "Ana", "Amy", "Dan", "Eli", "Rob", "Mya"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Mya finished above Eli" → Mya < Eli
problem.addConstraint(lambda Mya, Eli: Mya < Eli, ["Mya", "Eli"])

# "Eve finished below Rob" → Rob < Eve
problem.addConstraint(lambda Rob, Eve: Rob < Eve, ["Rob", "Eve"])

# "Amy finished second" → Amy == 2
problem.addConstraint(lambda Amy: Amy == 2, ["Amy"])

# "Rob finished below Dan" → Dan < Rob
problem.addConstraint(lambda Dan, Rob: Dan < Rob, ["Dan", "Rob"])

# "Ana finished second-to-last" → Ana == 6
problem.addConstraint(lambda Ana: Ana == 6, ["Ana"])

# "Dan finished fourth" → Dan == 4
problem.addConstraint(lambda Dan: Dan == 4, ["Dan"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfer names
choices = {
    "A": "Eve",
    "B": "Ana",
    "C": "Amy",
    "D": "Dan",
    "E": "Eli",
    "F": "Rob",
    "G": "Mya"
}

# Find who finished last (rank = 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)