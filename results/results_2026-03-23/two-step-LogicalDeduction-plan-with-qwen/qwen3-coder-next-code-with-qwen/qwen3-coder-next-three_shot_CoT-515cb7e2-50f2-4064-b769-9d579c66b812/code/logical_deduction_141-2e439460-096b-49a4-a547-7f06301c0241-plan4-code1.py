from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (placements 1-7, where 1 is first, 7 is last)
golfers = ["Joe", "Rob", "Eli", "Dan", "Mya", "Ada", "Ana"]
placements = range(1, 8)
problem.addVariables(golfers, placements)

# Add constraints
# All golfers have distinct placements
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana (Joe's placement < Ana's placement)
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# Ana finished second-to-last (placement = 6)
problem.addConstraint(lambda Ana: Ana == 6, ["Ana"])

# Mya finished fourth (placement = 4)
problem.addConstraint(lambda Mya: Mya == 4, ["Mya"])

# Dan finished third (placement = 3)
problem.addConstraint(lambda Dan: Dan == 3, ["Dan"])

# Ada finished second (placement = 2)
problem.addConstraint(lambda Ada: Ada == 2, ["Ada"])

# Eli finished third-to-last (placement = 5)
problem.addConstraint(lambda Eli: Eli == 5, ["Eli"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Joe",
    "B": "Rob",
    "C": "Eli",
    "D": "Dan",
    "E": "Mya",
    "F": "Ada",
    "G": "Ana"
}

# Find who finished last (placement = 7)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 7:
            print(letter)