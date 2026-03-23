from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
golfers = ["Ana", "Rob", "Joe"]
positions = range(1, 4)  # 1=first, 2=second, 3=third
problem.addVariables(golfers, positions)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "Joe finished above Ana" -> Joe's position < Ana's position
problem.addConstraint(lambda Joe, Ana: Joe < Ana, ["Joe", "Ana"])

# "Rob finished above Joe" -> Rob's position < Joe's position
problem.addConstraint(lambda Rob, Joe: Rob < Joe, ["Rob", "Joe"])

# Solve the problem
solutions = problem.getSolutions()

# Determine who finished second (position 2)
for solution in solutions:
    if solution["Ana"] == 2:
        print("A")
    elif solution["Rob"] == 2:
        print("B")
    elif solution["Joe"] == 2:
        print("C")