from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Amy", "Eve", "Ada", "Rob", "Dan", "Mel", "Joe"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add AllDifferent constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements
# Joe finished third
problem.addConstraint(lambda Joe: Joe == 3, ["Joe"])
# Dan finished last
problem.addConstraint(lambda Dan: Dan == 7, ["Dan"])
# Eve finished first
problem.addConstraint(lambda Eve: Eve == 1, ["Eve"])
# Mel finished below Rob (Mel has worse position than Rob)
problem.addConstraint(lambda Mel, Rob: Mel > Rob, ["Mel", "Rob"])
# Ada finished above Joe (Ada has better position than Joe)
problem.addConstraint(lambda Ada: Ada < 3, ["Ada"])
# Rob finished third-to-last (position 5 in a 7-person race)
problem.addConstraint(lambda Rob: Rob == 5, ["Rob"])

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to golfer names
choices = {
    "A": "Amy",
    "B": "Eve",
    "C": "Ada",
    "D": "Rob",
    "E": "Dan",
    "F": "Mel",
    "G": "Joe"
}

# Find who finished fourth (position 4)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 4:
            print(letter)