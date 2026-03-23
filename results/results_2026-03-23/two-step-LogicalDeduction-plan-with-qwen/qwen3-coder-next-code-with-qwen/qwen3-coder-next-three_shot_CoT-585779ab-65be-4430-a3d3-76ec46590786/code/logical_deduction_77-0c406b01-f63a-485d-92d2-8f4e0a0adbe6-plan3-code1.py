from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 5, where 1 = first place)
golfers = ["Rob", "Amy", "Eve", "Mya", "Ana"]
positions = range(1, 6)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Mya finished below Rob → Mya's position > Rob's position
problem.addConstraint(lambda Mya, Rob: Mya > Rob, ["Mya", "Rob"])

# Ana finished below Eve → Ana's position > Eve's position
problem.addConstraint(lambda Ana, Eve: Ana > Eve, ["Ana", "Eve"])

# Amy finished second → Amy's position = 2
problem.addConstraint(lambda Amy: Amy == 2, ["Amy"])

# Eve finished below Mya → Eve's position > Mya's position
problem.addConstraint(lambda Eve, Mya: Eve > Mya, ["Eve", "Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to golfers (second-to-last means position 4)
choices = {
    "A": "Rob",
    "B": "Amy",
    "C": "Eve",
    "D": "Mya",
    "E": "Ana"
}

# Find which golfer is in position 4 (second-to-last)
for solution in solutions:
    for letter, golfer in choices.items():
        if solution[golfer] == 4:
            print(letter)