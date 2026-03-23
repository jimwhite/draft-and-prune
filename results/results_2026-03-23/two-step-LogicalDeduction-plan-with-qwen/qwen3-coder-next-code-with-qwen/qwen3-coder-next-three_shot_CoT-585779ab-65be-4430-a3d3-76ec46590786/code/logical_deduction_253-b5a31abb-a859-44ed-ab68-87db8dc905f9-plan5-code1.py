from constraint import *

problem = Problem()

fruits = ["cantaloupe", "watermelon", "mango"]
ranks = range(1, 4)
problem.addVariables(fruits, ranks)

problem.addConstraint(AllDifferentConstraint())

problem.addConstraint(lambda mango: mango == 1, ["mango"])

problem.addConstraint(lambda cantaloupe: cantaloupe == 2, ["cantaloupe"])

solutions = problem.getSolutions()

solution = solutions[0]

print("A")