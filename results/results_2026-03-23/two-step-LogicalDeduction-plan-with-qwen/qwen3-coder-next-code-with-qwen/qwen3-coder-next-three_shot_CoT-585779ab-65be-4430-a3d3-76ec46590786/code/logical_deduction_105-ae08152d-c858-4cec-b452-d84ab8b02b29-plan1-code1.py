from constraint import *

# Initialize the problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 7=newest)
vehicles = ["station_wagon", "truck", "sedan", "limousine", "convertible", "bus", "hatchback"]
ranks = range(1, 8)
problem.addVariables(vehicles, ranks)

# Add all different constraint
problem.addConstraint(AllDifferentConstraint())

# Add constraints based on the problem statements:
# 1. The limousine is the newest → limousine == 7
problem.addConstraint(lambda limousine: limousine == 7, ["limousine"])

# 2. The bus is the third-newest → bus == 5 (7=newest, 6=second-newest, 5=third-newest)
problem.addConstraint(lambda bus: bus == 5, ["bus"])

# 3. The bus is older than the convertible → bus < convertible
problem.addConstraint(lambda bus, convertible: bus < convertible, ["bus", "convertible"])

# 4. The sedan is the third-oldest → sedan == 3
problem.addConstraint(lambda sedan: sedan == 3, ["sedan"])

# 5. The station wagon is older than the truck → station_wagon < truck
problem.addConstraint(lambda station_wagon, truck: station_wagon < truck, ["station_wagon", "truck"])

# 6. The hatchback is the oldest → hatchback == 1
problem.addConstraint(lambda hatchback: hatchback == 1, ["hatchback"])

# Solve the problem
solutions = problem.getSolutions()

# The question asks which vehicle is the third-oldest (rank 3)
# According to constraint #4, sedan == 3 must hold in any solution
# So we check which vehicle has rank 3 in the solution

for solution in solutions:
    for letter, vehicle_name in [
        ("A", "station_wagon"),
        ("B", "truck"),
        ("C", "sedan"),
        ("D", "limousine"),
        ("E", "convertible"),
        ("F", "bus"),
        ("G", "hatchback")
    ]:
        if solution[vehicle_name] == 3:
            print(letter)