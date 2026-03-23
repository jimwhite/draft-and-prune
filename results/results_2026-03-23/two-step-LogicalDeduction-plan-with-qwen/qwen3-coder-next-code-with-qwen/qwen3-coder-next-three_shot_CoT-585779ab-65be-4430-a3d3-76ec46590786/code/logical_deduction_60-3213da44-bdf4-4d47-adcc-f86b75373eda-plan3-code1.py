from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["bus", "truck", "motorcycle", "sedan", "hatchback"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The sedan is the second-oldest."
problem.addConstraint(lambda sedan: sedan == 2, ["sedan"])

# "The hatchback is newer than the motorcycle."
problem.addConstraint(lambda hatchback, motorcycle: hatchback > motorcycle, ["hatchback", "motorcycle"])

# "The motorcycle is newer than the sedan."
problem.addConstraint(lambda motorcycle, sedan: motorcycle > sedan, ["motorcycle", "sedan"])

# "The hatchback is older than the truck."
problem.addConstraint(lambda hatchback, truck: hatchback < truck, ["hatchback", "truck"])

# Solve the problem
solutions = problem.getSolutions()

# Check which vehicle is second-oldest (rank 2)
for solution in solutions:
    for choice_letter, vehicle in [("A", "bus"), ("B", "truck"), ("C", "motorcycle"), ("D", "sedan"), ("E", "hatchback")]:
        if solution[vehicle] == 2:
            print(choice_letter)