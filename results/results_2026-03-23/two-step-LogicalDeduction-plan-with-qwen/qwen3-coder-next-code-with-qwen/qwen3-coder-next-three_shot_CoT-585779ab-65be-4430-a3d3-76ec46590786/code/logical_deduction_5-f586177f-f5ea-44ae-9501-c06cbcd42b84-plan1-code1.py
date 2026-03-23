from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "sedan", "station_wagon", "bus", "limousine"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The sedan is newer than the station wagon" -> sedan > station_wagon
problem.addConstraint(lambda sedan, station_wagon: sedan > station_wagon, ["sedan", "station_wagon"])

# "The limousine is the newest" -> limousine == 5
problem.addConstraint(lambda limousine: limousine == 5, ["limousine"])

# "The bus is the second-newest" -> bus == 4
problem.addConstraint(lambda bus: bus == 4, ["bus"])

# "The convertible is the second-oldest" -> convertible == 2
problem.addConstraint(lambda convertible: convertible == 2, ["convertible"])

# Solve the problem
solutions = problem.getSolutions()

# Check which choice is true based on the solution
for solution in solutions:
    # Check each choice
    if solution["convertible"] == 2:
        print("A")
    elif solution["sedan"] == 2:
        print("B")
    elif solution["station_wagon"] == 2:
        print("C")
    elif solution["bus"] == 2:
        print("D")
    elif solution["limousine"] == 2:
        print("E")