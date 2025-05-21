from z3 import *

# Define variables
report_student = Function('report_student', IntSort(), IntSort(), IntSort())
gives_report = Function('gives_report', IntSort(), BoolSort())
days = [0, 1, 2]
times = [0, 1]
students = range(8)

solver = Solver()

# Constraint 1: Exactly 6 students give reports
solver.add(PbEq([(gives_report(i), 1) for i in students], 6))

# Constraint 2: Two reports per day
# Fixed: d and t must be declared as Ints inside the quantifier
solver.add(ForAll([d], Implies(And(d >= 0, d <= 2), PbEq([(report_student(d, t) != -1, 1) for t in times], 2))))


# Constraint 3: Link report_student and gives_report, and distinct reports
solver.add(ForAll([d, t], Implies(And(d >= 0, d <= 2, t >= 0, t <= 1, report_student(d, t) != -1), gives_report(report_student(d, t)))))
solver.add(ForAll([s], Implies(gives_report(s), PbEq([(And(d >= 0, d <= 2, t >= 0, t <= 1, report_student(d, t) == s)) for d in days for t in times], 1))))
solver.add(ForAll([s], Implies(Not(gives_report(s)), ForAll([d, t], Implies(And(d >= 0, d <= 2, t >= 0, t <= 1), report_student(d, t) != s)))))


# Constraint 4: George reports only on Tuesday
solver.add(ForAll([d, t], Implies(And(d >= 0, d <= 2, t >= 0, t <= 1, report_student(d, t) == 0), d == 2)))

# Constraint 5: Olivia and Robert not in afternoon
solver.add(ForAll([d], Implies(And(d >= 0, d <= 2), And(report_student(d, 1) != 6, report_student(d, 1) != 7))))

# Constraint 6: Nina's implication
solver.add(Implies(Or(report_student(0, 0) == 5, report_student(0, 1) == 5), And(Or(report_student(1, 0) == 1, report_student(1, 1) == 1), Or(report_student(1, 0) == 2, report_student(1, 1) == 2))))
solver.add(Implies(Or(report_student(1, 0) == 5, report_student(1, 1) == 5), And(Or(report_student(2, 0) == 1, report_student(2, 1) == 1), Or(report_student(2, 0) == 2, report_student(2, 1) == 2))))

# Constraint 7: George, Nina, Robert give reports
solver.add(gives_report(0))
solver.add(gives_report(5))
solver.add(gives_report(7))

# Constraint 8: George, Nina, Robert on different days
solver.add(Or(And(Or(report_student(0, 0) == 5, report_student(0, 1) == 5), Or(report_student(2, 0) == 7, report_student(2, 1) == 7)), And(Or(report_student(2, 0) == 5, report_student(2, 1) == 5), Or(report_student(0, 0) == 7, report_student(0, 1) == 7))))

# Check answer choices
answer_choices = [
    Or(report_student(2, 0) == 1, report_student(2, 1) == 1),  # A
    Or(report_student(0, 0) == 5, report_student(0, 1) == 5),  # B
    Or(report_student(1, 0) == 5, report_student(1, 1) == 5),  # C
    Or(report_student(0, 0) == 6, report_student(0, 1) == 6),  # D
    Or(report_student(2, 0) == 7, report_student(2, 1) == 7)   # E
]

for i, choice in enumerate(answer_choices):
    solver.push()
    solver.add(choice)
    if solver.check() == sat:
        print(f"Option {chr(65 + i)} is correct")
        exit()
    solver.pop()

