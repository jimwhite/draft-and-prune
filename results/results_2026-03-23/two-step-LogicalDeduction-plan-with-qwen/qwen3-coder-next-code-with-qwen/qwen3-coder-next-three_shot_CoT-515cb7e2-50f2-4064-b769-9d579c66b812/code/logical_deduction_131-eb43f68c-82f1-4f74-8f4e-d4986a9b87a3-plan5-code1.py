from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (golfers) and domain (positions 1 to 7)
golfers = ["Joe", "Mel", "Mya", "Eve", "Rob", "Ada", "Dan"]
positions = range(1, 8)
problem.addVariables(golfers, positions)

# Add AllDifferentConstraint to ensure unique positions
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the statements:
# "Rob finished first" → Rob's position = 1
problem.addConstraint(lambda Rob: Rob == 1, ["Rob"])

# "Eve finished last" → Eve's position = 7
problem.addConstraint(lambda Eve: Eve == 7, ["Eve"])

# "Dan finished above Ada" → Dan's position < Ada's position
problem.addConstraint(lambda Dan, Ada: Dan < Ada, ["Dan", "Ada"])

# "Mel finished above Mya" → Mel's position < Mya's position
problem.addConstraint(lambda Mel, Mya: Mel < Mya, ["Mel", "Mya"])

# "Joe finished second-to-last" → Joe's position = 6
problem.addConstraint(lambda Joe: Joe == 6, ["Joe"])

# "Mya finished third" → Mya's position = 3
problem.addConstraint(lambda Mya: Mya == 3, ["Mya"])

# Solve the problem
solutions = problem.getSolutions()

# Since we know Mya must be third (explicitly constrained), check the solution
solution = solutions[0]

# The question asks who finished third. We can directly check which golfer has position 3
for golfer, pos in solution.items():
    if pos == 3:
        # Map to the correct choice letter
        if golfer == "Mya":
            print("C")
        break