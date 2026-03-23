from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["sedan", "minivan", "motorcyle"]
ranks = range(1, 4)  # 1=oldest, 2=second-newest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The motorcyle is the second-newest"
problem.addConstraint(lambda motorcyle: motorcyle == 2, ["motorcyle"])

# "The minivan is newer than the motorcyle"
problem.addConstraint(lambda minivan, motorcyle: minivan > motorcyle, ["minivan", "motorcyle"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is second-newest (rank 2)
choices = {
    "A": "sedan",
    "B": "minivan",
    "C": "motorcyle"
}

# Find the vehicle with rank 2 and print its corresponding letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 2:
            print(letter)