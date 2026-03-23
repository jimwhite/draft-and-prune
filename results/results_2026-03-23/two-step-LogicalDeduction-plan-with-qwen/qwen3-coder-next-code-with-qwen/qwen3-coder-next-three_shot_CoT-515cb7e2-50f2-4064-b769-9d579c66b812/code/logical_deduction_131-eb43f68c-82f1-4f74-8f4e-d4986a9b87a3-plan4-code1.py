from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7, where 1 = first place)
golfers = ["Joe", "Mel", "Mya", "Eve", "Rob", "Ada", "Dan"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add all-different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# Rob finished first
problem.addConstraint(lambda Rob: Rob == 1, ["Rob"])

# Eve finished last
problem.addConstraint(lambda Eve: Eve == 7, ["Eve"])

# Dan finished above Ada (Dan's position < Ada's position)
problem.addConstraint(lambda Dan, Ada: Dan < Ada, ["Dan", "Ada"])

# Mel finished above Mya (Mel's position < Mya's position)
problem.addConstraint(lambda Mel, Mya: Mel < Mya, ["Mel", "Mya"])

# Joe finished second-to-last (position 6)
problem.addConstraint(lambda Joe: Joe == 6, ["Joe"])

# Mya finished third (position 3)
problem.addConstraint(lambda Mya: Mya == 3, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Find who finished third (position 3)
third_place_golfer = None
for solution in solutions:
    for golfer, position in solution.items():
        if position == 3:
            third_place_golfer = golfer
            break
    if third_place_golfer is not None:
        break

# Map choices to golfers
choices = {
    "A": "Joe",
    "B": "Mel",
    "C": "Mya",
    "D": "Eve",
    "E": "Rob",
    "F": "Ada",
    "G": "Dan"
}

# Find the choice letter corresponding to the golfer who finished third
for letter, golfer in choices.items():
    if golfer == third_place_golfer:
        print(letter)
        break