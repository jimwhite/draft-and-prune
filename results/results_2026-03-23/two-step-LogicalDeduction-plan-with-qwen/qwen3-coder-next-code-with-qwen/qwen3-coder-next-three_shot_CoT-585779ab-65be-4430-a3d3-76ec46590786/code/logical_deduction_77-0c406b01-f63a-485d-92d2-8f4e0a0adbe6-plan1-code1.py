from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (ranks 1 to 5, where 1 is best)
golfers = ["Rob", "Amy", "Eve", "Mya", "Ana"]
ranks = range(1, 6)
problem.addVariables(golfers, ranks)

# Add constraints
# All golfers have different ranks
problem.addConstraint(AllDifferentConstraint())

# "Mya finished below Rob" => Mya's rank > Rob's rank
problem.addConstraint(lambda Rob, Mya: Rob < Mya, ["Rob", "Mya"])

# "Ana finished below Eve" => Ana's rank > Eve's rank
problem.addConstraint(lambda Eve, Ana: Eve < Ana, ["Eve", "Ana"])

# "Amy finished second" => Amy's rank == 2
problem.addConstraint(lambda Amy: Amy == 2, ["Amy"])

# "Eve finished below Mya" => Eve's rank > Mya's rank
problem.addConstraint(lambda Mya, Eve: Mya < Eve, ["Mya", "Eve"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers (second-to-last means rank 4)
choices = {
    "A": "Rob",
    "B": "Amy",
    "C": "Eve",
    "D": "Mya",
    "E": "Ana"
}

# Find which golfer has rank 4 (second-to-last)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 4:
            print(letter)