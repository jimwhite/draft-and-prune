from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["station_wagon", "truck", "sedan", "limousine", "convertible", "bus", "hatchback"]
ranks = range(1, 8)  # 1=oldest, 7=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The limousine is the newest."
problem.addConstraint(lambda limousine: limousine == 7, ["limousine"])

# "The bus is the third-newest." (positions: 7=newest, 6=second-newest, 5=third-newest)
problem.addConstraint(lambda bus: bus == 5, ["bus"])

# "The bus is older than the convertible."
problem.addConstraint(lambda bus, convertible: bus < convertible, ["bus", "convertible"])

# "The sedan is the third-oldest."
problem.addConstraint(lambda sedan: sedan == 3, ["sedan"])

# "The station wagon is older than the truck."
problem.addConstraint(lambda station_wagon, truck: station_wagon < truck, ["station_wagon", "truck"])

# "The hatchback is the oldest."
problem.addConstraint(lambda hatchback: hatchback == 1, ["hatchback"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the third-oldest (rank 3)
# According to constraints, sedan must be rank 3
for solution in solutions:
    if solution["sedan"] == 3:
        print("C")