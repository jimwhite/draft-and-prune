from constraint import *

# Initialize the problem
problem = Problem()

# Define variables and domain
vehicles = ["convertible", "truck", "bus", "sedan", "motorcyle"]
ranks = range(1, 6)  # 1=oldest, 5=newest
problem.addVariables(vehicles, ranks)

# Add constraints
problem.addConstraint(AllDifferentConstraint())

# "The bus is newer than the truck" -> bus > truck
problem.addConstraint(lambda truck, bus: truck < bus, ["truck", "bus"])

# "The truck is newer than the convertible" -> truck > convertible
problem.addConstraint(lambda convertible, truck: convertible < truck, ["convertible", "truck"])

# "The sedan is the second-oldest" -> sedan == 2
problem.addConstraint(lambda sedan: sedan == 2, ["sedan"])

# "The motorcyle is newer than the bus" -> motorcyle > bus
problem.addConstraint(lambda bus, motorcyle: bus < motorcyle, ["bus", "motorcyle"])

# Solve the problem
solutions = problem.getSolutions()

# Map choices to vehicle names
choices = {
    "A": "convertible",
    "B": "truck",
    "C": "bus",
    "D": "sedan",
    "E": "motorcyle"
}

# Find the newest vehicle (rank 5) and print corresponding choice letter
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 5:
            print(letter)