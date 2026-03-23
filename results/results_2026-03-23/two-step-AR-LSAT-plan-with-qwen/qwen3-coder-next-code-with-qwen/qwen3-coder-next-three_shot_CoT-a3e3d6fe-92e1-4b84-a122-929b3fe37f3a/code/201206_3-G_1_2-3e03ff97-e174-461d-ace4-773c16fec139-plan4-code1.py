from z3 import *

# Assistant indices: Julio=0, Kevin=1, Lan=2, Nessa=3, Olivia=4, Rebecca=5
assistants = ["Julio", "Kevin", "Lan", "Nessa", "Olivia", "Rebecca"]
J, K, L, N, O, R = range(6)

# Session positions: 0-5 corresponding to [Wed AM, Wed PM, Thu AM, Thu PM, Fri AM, Fri PM]
pos = [Int(f"pos_{i}") for i in range(6)]

# Base solver
solver = Solver()

# Domain constraints: each position between 0 and 5, all distinct
for i in range(6):
    solver.add(pos[i] >= 0, pos[i] <= 5)
solver.add(Distinct(*pos))

# Day mapping helper: day(p) = p // 2 (0=Wed, 1=Thu, 2=Fri)
def day(p):
    return IntVal(p // 2) if isinstance(p, int) else p / 2

# Kevin and Rebecca same day
solver.add(day(pos[K]) == day(pos[R]))

# Lan and Olivia different days
solver.add(day(pos[L]) != day(pos[O]))

# Nessa afternoon session (positions 1, 3, 5)
solver.add(Or(pos[N] == 1, pos[N] == 3, pos[N] == 5))

# Julio earlier than Olivia
solver.add(pos[J] < pos[O])

# Premise: Lan does not lead a Wednesday session (day != 0)
solver.add(day(pos[L]) != 0)

# Answer choices indices: Rebecca=5, Olivia=4, Nessa=3, Kevin=1, Julio=0
answer_choices = [R, O, N, K, J]
choice_names = ["Rebecca", "Olivia", "Nessa", "Kevin", "Julio"]

# Check which assistants must lead a Thursday session (positions 2 or 3)
answer_index_list = []
for idx, assistant in enumerate(answer_choices):
    s_chk = Solver()
    s_chk.add(solver.assertions())
    
    # Add constraint: assistant is NOT on Thursday (i.e., not in positions 2 or 3)
    s_chk.add(Or(pos[assistant] == 0, pos[assistant] == 1, pos[assistant] == 4, pos[assistant] == 5))
    
    # If UNSAT, then assistant MUST be Thursday
    if s_chk.check() == unsat:
        answer_index_list.append(idx)

print(answer_index_list)