from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Joe", "Mel", "Mya", "Eve", "Rob", "Ada", "Dan"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Rob finished first
problem.addConstraint(lambda Rob: Rob == 1, ["Rob"])

# Eve finished last
problem.addConstraint(lambda Eve: Eve == 7, ["Eve"])

# Dan finished above Ada (Dan's position number < Ada's)
problem.addConstraint(lambda Dan, Ada: Dan < Ada, ["Dan", "Ada"])

# Mel finished above Mya (Mel's position number < Mya's)
problem.addConstraint(lambda Mel, Mya: Mel < Mya, ["Mel", "Mya"])

# Joe finished second-to-last (position 6)
problem.addConstraint(lambda Joe: Joe == 6, ["Joe"])

# Mya finished third (position 3)
problem.addConstraint(lambda Mya: Mya == 3, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfers
choices = {
    "A": "Joe",
    "B": "Mel",
    "C": "Mya",
    "D": "Eve",
    "E": "Rob",
    "F": "Ada",
    "G": "Dan"
}

# Find which golfer finished third-to-last (position 5)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 5:
            print(letter)