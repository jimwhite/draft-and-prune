from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "bus", "minivan", "truck", "sedan"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The convertible is newer than the truck" -> convertible > truck
problem.addConstraint(lambda convertible, truck: convertible > truck, ("convertible", "truck"))

# "The minivan is the newest" -> minivan == 5
problem.addConstraint(lambda minivan: minivan == 5, ("minivan",))

# "The bus is the third-newest" -> bus == 3
problem.addConstraint(lambda bus: bus == 3, ("bus",))

# "The truck is newer than the sedan" -> truck > sedan
problem.addConstraint(lambda truck, sedan: truck > sedan, ("truck", "sedan"))

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "convertible",
    "B": "bus",
    "C": "minivan",
    "D": "truck",
    "E": "sedan"
}

# Find which vehicle is second-newest (rank 4)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 4:
            print(letter)