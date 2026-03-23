from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 5, where 1 = first, 5 = last)
golfers = ["Eve", "Eli", "Joe", "Rob", "Mya"]
ranks = range(1, 6)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# Rob finished above Mya: Rob's rank < Mya's rank
problem.addConstraint(lambda Rob, Mya: Rob < Mya, ["Rob", "Mya"])

# Eve finished first: Eve's rank = 1
problem.addConstraint(lambda Eve: Eve == 1, ["Eve"])

# Joe finished above Eli: Joe's rank < Eli's rank
problem.addConstraint(lambda Joe, Eli: Joe < Eli, ["Joe", "Eli"])

# Joe finished below Mya: Joe's rank > Mya's rank
problem.addConstraint(lambda Joe, Mya: Joe > Mya, ["Joe", "Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Eve",
    "B": "Eli",
    "C": "Joe",
    "D": "Rob",
    "E": "Mya"
}

# Find who finished last (rank = 5)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)