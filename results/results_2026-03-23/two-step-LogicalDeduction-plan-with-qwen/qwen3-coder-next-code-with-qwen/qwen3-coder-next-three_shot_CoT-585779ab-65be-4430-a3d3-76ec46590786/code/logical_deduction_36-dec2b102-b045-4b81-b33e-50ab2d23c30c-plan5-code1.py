from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 5, where 1 = best/first, 5 = last)
golfers = ["Dan", "Amy", "Eve", "Ana", "Mya"]
ranks = range(1, 6)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# Dan finished above Eve: Dan's rank < Eve's rank
problem.addConstraint(lambda Dan, Eve: Dan < Eve, ("Dan", "Eve"))

# Dan finished below Mya: Mya's rank < Dan's rank
problem.addConstraint(lambda Mya, Dan: Mya < Dan, ("Mya", "Dan"))

# Amy finished third
problem.addConstraint(lambda Amy: Amy == 3, ("Amy",))

# Ana finished second-to-last (position 4 in a 5-person race)
problem.addConstraint(lambda Ana: Ana == 4, ("Ana",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Dan",
    "B": "Amy",
    "C": "Eve",
    "D": "Ana",
    "E": "Mya"
}

# Find who finished last (rank 5)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)