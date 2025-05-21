from z3 import *

# 1. Singer IDs and Slot Numbers
K, L, T, W, Y, Z = 0, 1, 2, 3, 4, 5

# 2. Audition Schedule Array
audition_schedule = Array('audition_schedule', IntSort(), IntSort())

# 3. Individual Slot Variables
slot_K, slot_L, slot_T, slot_W, slot_Y, slot_Z = Ints('slot_K slot_L slot_T slot_W slot_Y slot_Z')

# 4. Constraints for audition_schedule
solver = Solver()
i = Int('i')
solver.add(ForAll(i, Implies(And(i >= 1, i <= 6), And(audition_schedule[i] >= 0, audition_schedule[i] <= 5))))
solver.add(Distinct([audition_schedule[i] for i in range(1, 7)]))

# 5. Linking audition_schedule to individual slot variables
solver.add(audition_schedule[slot_K] == K)
solver.add(audition_schedule[slot_L] == L)
solver.add(audition_schedule[slot_T] == T)
solver.add(audition_schedule[slot_W] == W)
solver.add(audition_schedule[slot_Y] == Y)
solver.add(audition_schedule[slot_Z] == Z)


# Constraints for slot variables
for slot in [slot_K, slot_L, slot_T, slot_W, slot_Y, slot_Z]:
    solver.add(And(slot >= 1, slot <= 6))
solver.add(Distinct([slot_K, slot_L, slot_T, slot_W, slot_Y, slot_Z]))


# 6. Recorded Status Property
def IsRecorded(s):
    return Or(s == K, s == L)

# 7. Recorded Status Constraints
solver.add(Not(IsRecorded(audition_schedule[4])))
solver.add(IsRecorded(audition_schedule[5]))

# 8. Ordering Constraints
solver.add(slot_W < slot_K)
solver.add(slot_W < slot_L)
solver.add(slot_K < slot_T)
solver.add(slot_Z < slot_Y)


# 9. Check Answer Choices
options = [K, L, T, W, Z]  # Singers in the answer choices
option_letters = ['A', 'B', 'C', 'D', 'E']

for idx, singer in enumerate(options):
    solver.push()
    solver.add(audition_schedule[6] == singer)
    if solver.check() == sat:
        print(f"Option {option_letters[idx]} is correct")
        exit()
    solver.pop()