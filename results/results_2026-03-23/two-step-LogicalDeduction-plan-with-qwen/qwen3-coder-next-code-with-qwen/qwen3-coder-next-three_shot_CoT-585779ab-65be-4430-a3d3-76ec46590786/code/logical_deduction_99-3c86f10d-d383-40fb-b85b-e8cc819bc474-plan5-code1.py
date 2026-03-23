from constraint import *

# Initialize the constraint satisfaction problem
problem = Problem()

# Define variables (vehicles) and domain (age ranks: 1=oldest, 5=newest)
vehicles = ["convertible", "truck", "bus", "sedan", "motorcyle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

# Add constraints based on the problem statements
# 1. All vehicles have different age ranks
problem.addConstraint(AllDifferentConstraint())

# 2. "The bus is newer than the truck" → bus > truck
problem.addConstraint(lambda truck, bus: truck < bus, ("truck", "bus"))

# 3. "The truck is newer than the convertible" → truck > convertible
problem.addConstraint(lambda convertible, truck: convertible < truck, ("convertible", "truck"))

# 4. "The sedan is the second-oldest" → sedan == 2
problem.addConstraint(lambda sedan: sedan == 2, ("sedan",))

# 5. "The motorcyle is newer than the bus" → motorcyle > bus
problem.addConstraint(lambda bus, motorcyle: bus < motorcyle, ("bus", "motorcyle"))

# Solve the problem
solutions = problem.getSolutions()

# Map choice letters to vehicle names for third-newest (rank 3)
choices = {
    "A": "convertible",
    "B": "truck",
    "C": "bus",
    "D": "sedan",
    "E": "motorcyle"
}

# Find which vehicle has rank 3 (third-newest)
for solution in solutions:
    for letter, vehicle_name in choices.items():
        if solution[vehicle_name] == 3:
            print(letter)