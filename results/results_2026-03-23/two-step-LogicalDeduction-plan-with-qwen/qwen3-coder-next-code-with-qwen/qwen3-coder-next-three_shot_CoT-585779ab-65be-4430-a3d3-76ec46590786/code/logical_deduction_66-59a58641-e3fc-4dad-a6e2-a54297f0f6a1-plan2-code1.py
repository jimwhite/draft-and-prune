from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 5, where 1 = first, 5 = last)
golfers = ["Joe", "Eve", "Mya", "Rob", "Dan"]
ranks = range(1, 6)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# "Joe finished below Dan" -> Joe's rank > Dan's rank
problem.addConstraint(lambda Joe, Dan: Joe > Dan, ["Joe", "Dan"])

# "Mya finished first" -> Mya's rank = 1
problem.addConstraint(lambda Mya: Mya == 1, ["Mya"])

# "Dan finished below Rob" -> Dan's rank > Rob's rank
problem.addConstraint(lambda Dan, Rob: Dan > Rob, ["Dan", "Rob"])

# "Eve finished above Rob" -> Eve's rank < Rob's rank
problem.addConstraint(lambda Eve, Rob: Eve < Rob, ["Eve", "Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Joe",
    "B": "Eve",
    "C": "Mya",
    "D": "Rob",
    "E": "Dan"
}

# Find who finished last (rank = 5)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)