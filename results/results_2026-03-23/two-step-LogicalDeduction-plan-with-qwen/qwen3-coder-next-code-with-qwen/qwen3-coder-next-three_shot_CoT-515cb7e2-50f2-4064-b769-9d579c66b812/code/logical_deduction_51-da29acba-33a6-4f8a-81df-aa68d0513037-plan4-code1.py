from constraint import *

problem = Problem()

vehicles = ["minivan", "hatchback", "bus", "convertible", "motorcyle"]
ranks = range(1, 6)
problem.addVariables(vehicles, ranks)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda hatchback, convertible: hatchback > convertible, ("hatchback", "convertible"))

problem.addConstraint(lambda bus, hatchback: bus > hatchback, ("bus", "hatchback"))

problem.addConstraint(lambda bus, motorcyle: bus < motorcyle, ("bus", "motorcyle"))

problem.addConstraint(lambda minivan: minivan == 5, ("minivan",))

solutions = problem.getSolutions()

print("A")