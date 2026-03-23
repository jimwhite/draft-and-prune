from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (golfers) and domain (finishing positions: 1=first, 2=second, 3=last)
golfers = ["Ana", "Rob", "Joe"]
positions = range(1, 4)
problem.addVariables(golfers, positions)

# Add constraints
# All golfers must have different finishing positions
problem.addConstraint(AllDifferentConstraint())

# Joe finished above Ana (Joe's position number < Ana's position number)
problem.addConstraint(lambda j, a: j < a, ("Joe", "Ana"))

# Rob finished second
problem.addConstraint(lambda r: r == 2, ("Rob",))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to statements (we need to find who finished last, i.e., position 3)
# The question asks which statement is true, so we check who has position 3
choices = {
    "A": "Ana",
    "B": "Rob",
    "C": "Joe"
}

# Find the golfer with position 3 (last place)
for solution in solutions:
    for letter, golfer_name in choices.items():
        if solution[golfer_name] == 3:
            print(letter)