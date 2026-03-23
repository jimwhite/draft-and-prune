from constraint import *

# Set up the problem environment
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "tractor", "hatchback"]
ranks = range(1, 4)  # 1=oldest, 3=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The hatchback is older than the convertible"
problem.addConstraint(lambda hatchback, convertible: hatchback < convertible, ("hatchback", "convertible"))

# "The tractor is the newest"
problem.addConstraint(lambda tractor: tractor == 3, ("tractor",))

# Solve for the arrangement
solutions = problem.getSolutions()
solution = solutions[0]

# Determine which vehicle is the second-newest (rank 2)
choices = {
    "A": "convertible",
    "B": "tractor",
    "C": "hatchback"
}

for letter, vehicle_name in choices.items():
    if solution[vehicle_name] == 2:
        print(letter)