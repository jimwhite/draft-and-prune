from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 7, where 1 is best, 7 is worst)
golfers = ["Joe", "Rob", "Eli", "Dan", "Mya", "Ada", "Ana"]
ranks = range(1, 8)
problem.addVariables(golfers, ranks)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Joe finished above Ana → Joe's rank < Ana's rank
problem.addConstraint(lambda j, a: j < a, ["Joe", "Ana"])

# Ana finished second-to-last → rank = 6
problem.addConstraint(lambda a: a == 6, ["Ana"])

# Mya finished fourth → rank = 4
problem.addConstraint(lambda m: m == 4, ["Mya"])

# Dan finished third → rank = 3
problem.addConstraint(lambda d: d == 3, ["Dan"])

# Ada finished second → rank = 2
problem.addConstraint(lambda a: a == 2, ["Ada"])

# Eli finished third-to-last → rank = 5 (since 7=last, 6=second-to-last, 5=third-to-last)
problem.addConstraint(lambda e: e == 5, ["Eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers
choices = {
    "A": "Joe",
    "B": "Rob",
    "C": "Eli",
    "D": "Dan",
    "E": "Mya",
    "F": "Ada",
    "G": "Ana"
}

# Find who finished last (rank 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)