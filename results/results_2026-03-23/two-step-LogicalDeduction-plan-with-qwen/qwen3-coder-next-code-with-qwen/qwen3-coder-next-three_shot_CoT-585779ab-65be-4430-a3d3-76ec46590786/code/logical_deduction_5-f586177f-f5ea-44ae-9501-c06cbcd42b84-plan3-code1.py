from constraint import *

# Initialize the problem environment
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["convertible", "sedan", "station_wagon", "bus", "limousine"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the statements
# All vehicles must have different ranks
problem.addConstraint(AllDifferentConstraint())

# "The sedan is newer than the station wagon" → sedan > station_wagon
problem.addConstraint(lambda sedan, station_wagon: sedan > station_wagon, ("sedan", "station_wagon"))

# "The limousine is the newest" → limousine == 5
problem.addConstraint(lambda limousine: limousine == 5, ("limousine",))

# "The bus is the second-newest" → bus == 4
problem.addConstraint(lambda bus: bus == 4, ("bus",))

# "The convertible is the second-oldest" → convertible == 2
problem.addConstraint(lambda convertible: convertible == 2, ("convertible",))

# Solve the problem
solutions = problem.getSolutions()

# The question asks which statement is true, with choices mapping to vehicles
# Since the constraint directly sets convertible == 2 (second-oldest),
# and option A states exactly that, we verify by checking the solution
for solution in solutions:
    # Check which vehicle has rank 2 (second-oldest)
    for letter, vehicle in [("A", "convertible"), ("B", "sedan"), ("C", "station_wagon"), 
                            ("D", "bus"), ("E", "limousine")]:
        if solution[vehicle] == 2:
            print(letter)